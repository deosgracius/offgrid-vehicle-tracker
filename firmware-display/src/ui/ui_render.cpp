#include "ui_render.h"
#include "../protocol/tracker_store.h"
#include "../protocol/node_table.h"
#include "../nav/nav.h"
#include "../nav/dead_reckon.h"
#include "../nav/local_time.h"
#include "rlcd.h"
#include <Arduino.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Driver display — two pages, toggled by TAPPING the KEY button (leftmost):
//   Page 0  NAV: heading-up compass (cardinals rotate with the vehicle like a
//           real car compass), partner arrow relative to the nose, distance in
//           miles, blinker chevrons when the partner is off-axis, and a
//           CHANGE COURSE warning if off-axis persists ~5 s (clears on course).
//   Page 1  STATUS ("OVERALL TRACKER"): centered ME/PTR fixes, distance in
//           miles, partner's compass direction from you.
// HOLDING KEY ~1 s (instead of tapping) still fires the tracking reset.
#define TRACK_RESET_PIN 18
#define STALE_AGE_S     120
#define MESH_FRESH_S    90      // partner heard within this = "SF<->RG OK"
#define MSG_POPUP_MS    8000    // mesh text message stays on screen this long
#define BLINK_DEG       30.0f   // |arrow| beyond this -> blinker on
#define WARN_DEG        45.0f   // |arrow| beyond this counts toward warning
#define WARN_ON_TICKS   10      // 10 x 500 ms = 5 s off-course -> warning
#define WARN_CLEAR_DEG  30.0f   // back within this -> warning clears

static bool s_have_panel = false;
static int  s_page = 0;

void ui_render_init(void) {
    pinMode(TRACK_RESET_PIN, INPUT_PULLUP);
    s_have_panel = rlcd_init();
    Serial.printf("[ui] RLCD init %s\n", s_have_panel ? "OK" : "FAILED (serial only)");
    if (s_have_panel) {
        rlcd_clear(true);
        rlcd_draw_text(24, 120, "GROUP 9 TRACKER", 3, false);
        rlcd_draw_text(24, 160, "starting up...", 2, false);
        rlcd_flush();
    }
}

// ---- drawing helpers -------------------------------------------------------

static void ctext(int y, const char *s, int scale, bool white) {
    int w = (int)strlen(s) * 8 * scale;
    rlcd_draw_text((RLCD_W - w) / 2, y, s, scale, white);
}

static void fill_triangle(float x0, float y0, float x1, float y1,
                          float x2, float y2, bool white) {
    int minx = (int)floorf(fminf(x0, fminf(x1, x2)));
    int maxx = (int)ceilf(fmaxf(x0, fmaxf(x1, x2)));
    int miny = (int)floorf(fminf(y0, fminf(y1, y2)));
    int maxy = (int)ceilf(fmaxf(y0, fmaxf(y1, y2)));
    float area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0);
    if (fabsf(area) < 0.01f) return;
    for (int y = miny; y <= maxy; y++)
        for (int x = minx; x <= maxx; x++) {
            float w0 = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0);
            float w1 = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1);
            float w2 = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2);
            bool in = (w0 >= 0 && w1 >= 0 && w2 >= 0) || (w0 <= 0 && w1 <= 0 && w2 <= 0);
            if (in) rlcd_set_pixel(x, y, white);
        }
}

static void draw_seg(float x0, float y0, float x1, float y1) {
    // Bresenham-ish segment via set_pixel, 2px thick for visibility
    float dx = x1 - x0, dy = y1 - y0;
    int n = (int)fmaxf(fabsf(dx), fabsf(dy));
    if (n < 1) n = 1;
    for (int i = 0; i <= n; i++) {
        int x = (int)(x0 + dx * i / n), y = (int)(y0 + dy * i / n);
        rlcd_set_pixel(x, y, false);
        rlcd_set_pixel(x + 1, y, false);
        rlcd_set_pixel(x, y + 1, false);
    }
}

// solid = live data; hollow outline = position is projected/aging (the dart
// stays honest: confident fill only while the fix is fresh).
static void draw_arrow(int cx, int cy, float R, float deg, bool solid) {
    // dart vertically centered: tip at +0.62R, tail barbs at -0.62R
    float a = deg * (float)M_PI / 180.0f, ca = cosf(a), sa = sinf(a);
    const float px[4] = {0.0f,  0.5f * R, 0.0f,      -0.5f * R};
    const float py[4] = {0.62f * R, -0.62f * R, -0.34f * R, -0.62f * R};
    float sx[4], sy[4];
    for (int i = 0; i < 4; i++) {
        float rx = px[i] * ca + py[i] * sa, ry = -px[i] * sa + py[i] * ca;
        sx[i] = cx + rx; sy[i] = cy - ry;
    }
    if (solid) {
        fill_triangle(sx[0], sy[0], sx[1], sy[1], sx[2], sy[2], false);
        fill_triangle(sx[0], sy[0], sx[2], sy[2], sx[3], sy[3], false);
    } else {
        draw_seg(sx[0], sy[0], sx[1], sy[1]);
        draw_seg(sx[1], sy[1], sx[2], sy[2]);
        draw_seg(sx[2], sy[2], sx[3], sy[3]);
        draw_seg(sx[3], sy[3], sx[0], sy[0]);
    }
}

static void fmt_miles(float m, char *out, size_t olen) {
    float mi = m / 1609.344f;
    if (mi >= 10.0f)      snprintf(out, olen, "%.0f mi", mi);
    else if (mi >= 0.15f) snprintf(out, olen, "%.2f mi", mi);
    else                  snprintf(out, olen, "%.0f ft", m * 3.28084f);
}

static void fmt_age(uint32_t s, char *out, size_t olen) {
    if (s < 60)        snprintf(out, olen, "%lus", (unsigned long)s);
    else if (s < 3600) snprintf(out, olen, "%lum", (unsigned long)(s / 60));
    else               snprintf(out, olen, "%luh", (unsigned long)(s / 3600));
}

static const char *cardinal8(float deg) {
    static const char *pts[8] = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"};
    int i = (int)floorf(nav_wrap360(deg + 22.5f) / 45.0f) % 8;
    return pts[i];
}

static void banner(int y, const char *txt) {
    rlcd_fill_rect(0, y, RLCD_W, 26, false);
    ctext(y + 5, txt, 2, true);
}

// Blinker chevrons at the top corners. dir: -1 left, +1 right. hard doubles it.
static void draw_blinker(int dir, bool hard, bool phase) {
    if (!phase) return; // blink at render rate
    // below the banner zone (banners end at y=54)
    int tipx  = dir < 0 ? 10 : RLCD_W - 10;
    int backx = dir < 0 ? 52 : RLCD_W - 52;
    fill_triangle(tipx, 74, backx, 58, backx, 90, false);
    if (hard) { // second chevron = "hard" turn
        fill_triangle(backx - dir * 8, 74, backx - dir * 38, 58, backx - dir * 38, 90, false);
    }
}

// ---- pages -----------------------------------------------------------------

// Radio callsigns when learned (e.g. "SF", "RG"); generic labels until then.
static const char *pname(const TrackerState &st) {
    return st.partner_name[0] ? st.partner_name : "PARTNER";
}
static const char *sname(const TrackerState &st) {
    return st.self_name[0] ? st.self_name : "YOU";
}

// "Both radios communicating" = the partner's data is fresh. The display rides
// on SF, so this directly proves SF hears RG; in a 2-node mesh the reverse
// direction is symmetric (and was proven by round-trip traceroute).
static bool mesh_ok(const TrackerState &st) {
    return st.partner.valid && st.partner.age_s <= MESH_FRESH_S;
}

// Small top-right tag, e.g. "SF<->RG OK", drawn only while the link is fresh.
static void draw_mesh_tag(const TrackerState &st) {
    if (!mesh_ok(st)) return;
    char buf[24];
    snprintf(buf, sizeof(buf), "%s<->%s OK", sname(st), pname(st));
    rlcd_draw_text(RLCD_W - (int)strlen(buf) * 8 - 6, 8, buf, 1, false);
}

static void render_nav(const TrackerState &st, const NavOutput &nav,
                       bool warn, bool phase, bool trend_ok, float trend_mph) {
    char buf[48], dist[16], age[12];
    rlcd_clear(true);
    ctext(6, pname(st), 2, false);
    draw_mesh_tag(st);

    // Compass, left side. COURSE-UP while driving: the top of the ring is
    // always straight ahead, so the dart reads like a windshield pointer
    // (dart up = partner dead ahead) and the cardinal letters rotate around
    // the ring -- heading south puts S at the top, exactly like a car's
    // navigation display. The driver never has to rotate the unit or do the
    // mental N-up transform. While stopped there is no nose to be relative
    // to, so the ring falls back to north-up with the dart at absolute
    // bearing (matching the "SE of you" wording used when parked).
    const int cx = 100, cy = 172, RING = 68;
    rlcd_draw_circle(cx, cy, RING, 2, false);
    {
        static const char *card[4] = {"N", "E", "S", "W"};
        float rot = nav.heading_valid ? st.self.course_deg : 0.0f;
        for (int i = 0; i < 4; i++) {
            float a = ((float)i * 90.0f - rot) * (float)M_PI / 180.0f;
            int lx = cx + (int)lroundf(sinf(a) * (RING + 17)) - 7;
            int ly = cy - (int)lroundf(cosf(a) * (RING + 17)) - 8;
            rlcd_draw_text(lx, ly, card[i], 2, false);
        }
    }
    if (nav.heading_valid) {
        draw_arrow(cx, cy, RING - 14, nav.arrow_deg,         // partner vs nose
                   st.partner.age_s <= 30);                  // hollow = projected
        // fixed index mark at 12 o'clock = your hood
        fill_triangle(cx - 6, cy - RING + 1, cx + 6, cy - RING + 1,
                      cx, cy - RING + 12, false);
    } else {
        draw_arrow(cx, cy, RING - 14, nav.bearing_deg,       // absolute bearing
                   st.partner.age_s <= 30);
    }

    // blinkers from the RELATIVE angle (driving only)
    if (nav.heading_valid && fabsf(nav.arrow_deg) > BLINK_DEG) {
        draw_blinker(nav.arrow_deg > 0 ? 1 : -1, fabsf(nav.arrow_deg) > 90.0f, phase);
    }

    // right column, clear of the ring — glanceable hierarchy for driving:
    //   huge distance, then WHERE in words, then data age, then own speed.
    fmt_miles(nav.distance_m, dist, sizeof(dist));
    int w = (int)strlen(dist) * 8 * 4;
    rlcd_draw_text(RLCD_W - w - 10, 92, dist, 4, false);  // below blinker zone

    // "where" in words: clock position while driving (relative to the nose),
    // compass cardinal while stopped (no heading to be relative to).
    if (nav.heading_valid) {
        int hour = (int)roundf(nav_wrap360(nav.arrow_deg) / 30.0f) % 12;
        if (hour == 0) hour = 12;
        snprintf(buf, sizeof(buf), "at %d o'clock", hour);
    } else {
        snprintf(buf, sizeof(buf), "%s of you", cardinal8(nav.bearing_deg));
    }
    rlcd_draw_text(RLCD_W - (int)strlen(buf) * 16 - 10, 128, buf, 2, false);

    // data age — inverted (white-on-black) past 30 s as an early staleness cue
    fmt_age(st.partner.age_s, age, sizeof(age));
    snprintf(buf, sizeof(buf), "age %s", age);
    {
        int tw = (int)strlen(buf) * 16;
        bool aging = st.partner.age_s > 30;
        if (aging) rlcd_fill_rect(RLCD_W - tw - 14, 154, tw + 8, 22, false);
        rlcd_draw_text(RLCD_W - tw - 10, 157, buf, 2, aging);
    }

    // own speed, so the driving page never needs a page flip
    if (st.self.valid) {
        snprintf(buf, sizeof(buf), "you %.0f mph", st.self.speed_mps * 2.23694f);
        rlcd_draw_text(RLCD_W - (int)strlen(buf) * 16 - 10, 186, buf, 2, false);
    }

    // closing/separating trend — the number a convoy driver actually watches
    if (trend_ok) {
        if (trend_mph > 2.0f)       snprintf(buf, sizeof(buf), "closing %.0f mph", trend_mph);
        else if (trend_mph < -2.0f) snprintf(buf, sizeof(buf), "apart %.0f mph", -trend_mph);
        else                        snprintf(buf, sizeof(buf), "holding");
        rlcd_draw_text(RLCD_W - (int)strlen(buf) * 16 - 10, 210, buf, 2, false);
    }

    if (nav.heading_valid) {
        snprintf(buf, sizeof(buf), "needle = %s", sname(st));
        rlcd_draw_text(216, 240, buf, 1, false);
        snprintf(buf, sizeof(buf), "dart   = %s", pname(st));
        rlcd_draw_text(216, 256, buf, 1, false);
    } else {
        rlcd_draw_text(RLCD_W - 7 * 16 - 10, 238, "stopped", 2, false);
    }

    // priority banners
    if (!st.ble_connected) {
        banner(28, "RADIO LINK LOST");
    } else if (st.partner.age_s > STALE_AGE_S) {
        snprintf(buf, sizeof(buf), "%s DATA STALE", pname(st));
        banner(28, buf);
    }
    else if (warn)
        banner(28, nav.arrow_deg > 0 ? "CHANGE COURSE >>" : "<< CHANGE COURSE");
    else if (st.partner_batt <= 20) {  // partner's radio about to die
        snprintf(buf, sizeof(buf), "%s BATTERY %u%%", pname(st), st.partner_batt);
        banner(28, buf);
    }

    snprintf(buf, sizeof(buf), "link %s - tap:next hold:reset",
             st.ble_connected ? "OK" : "LOST");
    rlcd_draw_text(8, 288, buf, 1, false);
}

static void render_status(const TrackerState &st, const NavOutput &nav) {
    char buf[48], age[12], dist[16];
    rlcd_clear(true);
    ctext(8, "OVERALL TRACKER", 2, false);
    ctext(42, st.ble_connected ? "LINK CONNECTED" : "LINK SEARCHING...", 2, false);
    if (mesh_ok(st)) {
        snprintf(buf, sizeof(buf), "radios: %s<->%s COMMUNICATING",
                 st.self_name[0] ? st.self_name : "ME",
                 st.partner_name[0] ? st.partner_name : "PTR");
    } else if (st.partner.valid) {
        char qage[12];
        fmt_age(st.partner.age_s, qage, sizeof(qage));
        snprintf(buf, sizeof(buf), "radios: quiet for %s", qage);
    } else {
        snprintf(buf, sizeof(buf), "radios: no contact yet");
    }
    ctext(64, buf, 1, false);

    const char *me  = st.self_name[0]    ? st.self_name    : "ME";
    const char *ptr = st.partner_name[0] ? st.partner_name : "PTR";
    if (st.self.valid) {
        snprintf(buf, sizeof(buf), "%-3s %.5f %.5f", me, st.self.lat_deg, st.self.lon_deg);
        ctext(80, buf, 2, false);
        fmt_age(st.self.age_s, age, sizeof(age));
        if (st.self_batt <= 100)
            snprintf(buf, sizeof(buf), "spd %.0f mph - %s - %u%%",
                     st.self.speed_mps * 2.23694f, age, st.self_batt);
        else
            snprintf(buf, sizeof(buf), "spd %.0f mph - age %s",
                     st.self.speed_mps * 2.23694f, age);
        ctext(104, buf, 2, false);
    } else {
        snprintf(buf, sizeof(buf), "%-3s waiting for GPS fix", me);
        ctext(80, buf, 2, false);
    }

    if (st.partner.valid) {
        snprintf(buf, sizeof(buf), "%-3s %.5f %.5f", ptr, st.partner.lat_deg, st.partner.lon_deg);
        ctext(142, buf, 2, false);
        fmt_age(st.partner.age_s, age, sizeof(age));
        if (st.partner_batt <= 100)
            snprintf(buf, sizeof(buf), "age %s - batt %u%%", age, st.partner_batt);
        else
            snprintf(buf, sizeof(buf), "age %s", age);
        ctext(166, buf, 2, false);
    } else {
        snprintf(buf, sizeof(buf), "%-3s not heard yet", ptr);
        ctext(142, buf, 2, false);
    }

    if (nav.valid) {
        fmt_miles(nav.distance_m, dist, sizeof(dist));
        ctext(200, dist, 5, false);
        snprintf(buf, sizeof(buf), "%s IS %s OF %s", ptr, cardinal8(nav.bearing_deg), me);
        ctext(250, buf, 2, false);
    }
    rlcd_draw_text(8, 282, "tap:messages hold:reset", 1, false);
}

static void render_messages(const TrackerState &st) {
    char buf[64], age[12];
    rlcd_clear(true);
    ctext(8, "MESSAGES", 2, false);
    if (st.msg_hist_n == 0) {
        ctext(140, "no messages", 2, false);
    } else {
        for (int i = 0; i < st.msg_hist_n && i < TRACKER_MSG_HIST; i++) {
            int y = 52 + i * 56;
            fmt_age((millis() - st.msg_hist[i].ms) / 1000UL, age, sizeof(age));
            snprintf(buf, sizeof(buf), "%s - %s ago", st.msg_hist[i].from, age);
            rlcd_draw_text(10, y, buf, 1, false);
            snprintf(buf, sizeof(buf), "%.24s", st.msg_hist[i].text);
            rlcd_draw_text(10, y + 14, buf, 2, false);
            rlcd_fill_rect(10, y + 36, RLCD_W - 20, 1, false);
        }
    }
    rlcd_draw_text(8, 282, "tap:compass hold:CLEAR ALL", 1, false);
}

static void render_searching(const TrackerState &st) {
    char buf[48];
    rlcd_clear(true);
    snprintf(buf, sizeof(buf), "SEARCHING FOR %s", pname(st));
    ctext(96, buf, 2, false);
    snprintf(buf, sizeof(buf), "radio link: %s", st.ble_connected ? "connected" : "connecting...");
    ctext(140, buf, 2, false);
    snprintf(buf, sizeof(buf), "own GPS:  %s", st.self.valid ? "locked" : "acquiring...");
    ctext(168, buf, 2, false);
}

// ---- task ------------------------------------------------------------------

void ui_render_task(void *arg) {
    (void)arg;
    char up[16];
    int tick = 0, held = 0, flash_ticks = 0, off_ticks = 0;
    bool warn = false;
    const char *flash_msg = "TRACKING RESET";
    // closing/separating trend state (EMA over ~5 s of 500 ms samples)
    float trend_ema_mps = 0.0f, prev_dist_m = 0.0f;
    bool trend_ok = false, trend_have_prev = false;

    for (;;) {
        // KEY: tap = next page, hold ~1 s = reset (messages page: clear history)
        if (digitalRead(TRACK_RESET_PIN) == LOW) {
            if (++held == 2) {
                if (s_page == 2) { node_table_clear_messages(); flash_msg = "MESSAGES CLEARED"; }
                else             { node_table_reset();          flash_msg = "TRACKING RESET"; }
                flash_ticks = 4;
            }
        } else {
            if (held == 1) s_page = (s_page + 1) % 3; // released after a short tap
            held = 0;
        }

        TrackerState st;
        tracker_store_get(&st);
        dr_apply(&st);  // project both fixes forward along course/speed (age untouched)
        NavOutput nav = nav_compute(&st);

        // distance-rate: positive = closing. Only meaningful on live-ish data.
        if (nav.valid && st.partner.age_s <= STALE_AGE_S) {
            if (trend_have_prev) {
                float rate = (prev_dist_m - nav.distance_m) / 0.5f;  // m/s, 500 ms ticks
                trend_ema_mps = 0.9f * trend_ema_mps + 0.1f * rate;
                trend_ok = true;
            }
            prev_dist_m = nav.distance_m;
            trend_have_prev = true;
        } else {
            trend_ok = false;
            trend_have_prev = false;
            trend_ema_mps = 0.0f;
        }

        // off-course warning state machine (5 s on, clears when back on course)
        if (nav.valid && nav.heading_valid && fabsf(nav.arrow_deg) > WARN_DEG) {
            if (off_ticks < 100) off_ticks++;
            if (!warn && off_ticks >= WARN_ON_TICKS) warn = true;
        } else if (nav.valid && nav.heading_valid && fabsf(nav.arrow_deg) <= WARN_CLEAR_DEG) {
            off_ticks = 0; warn = false;
        }
        if (!nav.valid || !nav.heading_valid) { off_ticks = 0; warn = false; }

        if (s_have_panel) {
            if (!nav.valid && s_page == 0) render_searching(st);
            else if (s_page == 0)          render_nav(st, nav, warn, (tick & 1) == 0,
                                                      trend_ok, trend_ema_mps * 2.23694f);
            else if (s_page == 1)          render_status(st, nav);
            else                           render_messages(st);
            if (flash_ticks > 0) {
                flash_ticks--;
                rlcd_fill_rect(0, 130, RLCD_W, 34, false);
                ctext(139, flash_msg, 2, true);
            }
            // Mesh text popup: "RG: Hi" for a few seconds after reception.
            if (st.msg_seq != 0 && (millis() - st.msg_ms) < MSG_POPUP_MS) {
                char msg[64];
                snprintf(msg, sizeof(msg), "%s: %.32s", st.msg_from, st.msg_text);
                if ((int)strlen(msg) * 16 > RLCD_W - 8)  // too wide at scale 2
                    msg[(RLCD_W - 8) / 16] = '\0';
                rlcd_fill_rect(0, 104, RLCD_W, 34, false);
                ctext(113, msg, 2, true);
            }
            // location-aware clock, top-left (GPS UTC -> local zone by position)
            if (st.utc_epoch != 0) {
                uint32_t now_epoch = st.utc_epoch;
                if (st.utc_ref_ms != 0) now_epoch += (millis() - st.utc_ref_ms) / 1000;
                double clat = st.self.valid ? st.self.lat_deg : 33.58;   // fallback: last-known region
                double clon = st.self.valid ? st.self.lon_deg : -101.86;
                char clock[20];
                if (local_time_fmt(now_epoch, clat, clon, clock, sizeof(clock)))
                    rlcd_draw_text(6, 2, clock, 1, false);
            }
            snprintf(up, sizeof(up), "up %lus", (unsigned long)(millis() / 1000));
            rlcd_draw_text(RLCD_W - 8 * (int)strlen(up) - 4, 288, up, 1, false);
            rlcd_flush();
        }

        if ((tick++ & 1) == 0) {
            if (!nav.valid) {
                Serial.printf("[ui] waiting for fix   ble=%d\n", st.ble_connected);
            } else {
                Serial.printf("[ui] pg%d arrow %+7.1f deg dist %7.0f m age %4lus ble=%d%s\n",
                              s_page, nav.heading_valid ? nav.arrow_deg : nav.bearing_deg,
                              nav.distance_m, (unsigned long)st.partner.age_s,
                              st.ble_connected, warn ? " WARN" : "");
            }
        }
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
