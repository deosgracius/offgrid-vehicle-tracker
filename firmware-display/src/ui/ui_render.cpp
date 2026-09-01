#include "ui_render.h"
#include "../protocol/tracker_store.h"
#include "../protocol/node_table.h"
#include "../nav/nav.h"
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

static void draw_arrow(int cx, int cy, float R, float deg) {
    // dart vertically centered: tip at +0.62R, tail barbs at -0.62R
    float a = deg * (float)M_PI / 180.0f, ca = cosf(a), sa = sinf(a);
    const float px[4] = {0.0f,  0.5f * R, 0.0f,      -0.5f * R};
    const float py[4] = {0.62f * R, -0.62f * R, -0.34f * R, -0.62f * R};
    float sx[4], sy[4];
    for (int i = 0; i < 4; i++) {
        float rx = px[i] * ca + py[i] * sa, ry = -px[i] * sa + py[i] * ca;
        sx[i] = cx + rx; sy[i] = cy - ry;
    }
    fill_triangle(sx[0], sy[0], sx[1], sy[1], sx[2], sy[2], false);
    fill_triangle(sx[0], sy[0], sx[2], sy[2], sx[3], sy[3], false);
}

// Thin needle showing OWN heading (tip at radius R, slim base).
static void draw_needle(int cx, int cy, float R, float deg) {
    float a = deg * (float)M_PI / 180.0f, ca = cosf(a), sa = sinf(a);
    const float px[3] = {0.0f, 4.0f, -4.0f};
    const float py[3] = {R, -0.15f * R, -0.15f * R};
    float sx[3], sy[3];
    for (int i = 0; i < 3; i++) {
        float rx = px[i] * ca + py[i] * sa, ry = -px[i] * sa + py[i] * ca;
        sx[i] = cx + rx; sy[i] = cy - ry;
    }
    fill_triangle(sx[0], sy[0], sx[1], sy[1], sx[2], sy[2], false);
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

static void render_nav(const TrackerState &st, const NavOutput &nav,
                       bool warn, bool phase) {
    char buf[48], dist[16], age[12];
    rlcd_clear(true);
    ctext(6, "PARTNER", 2, false);

    // North-up compass, left side. Two INDEPENDENT pointers:
    //   fat dart   = partner's absolute bearing (moves when THEY move)
    //   thin needle = own course               (swings live as YOU turn)
    // Steer until the needle covers the dart.
    const int cx = 100, cy = 172, RING = 68;
    rlcd_draw_circle(cx, cy, RING, 2, false);
    rlcd_draw_text(cx - 7,        cy - RING - 22, "N", 2, false);
    rlcd_draw_text(cx + RING + 8, cy - 8,         "E", 2, false);
    rlcd_draw_text(cx - 7,        cy + RING + 6,  "S", 2, false);
    rlcd_draw_text(cx - RING - 24, cy - 8,        "W", 2, false);

    draw_arrow(cx, cy, RING - 14, nav.bearing_deg);          // partner
    if (nav.heading_valid) {
        draw_needle(cx, cy, RING - 4, st.self.course_deg);   // me
    }

    // blinkers from the RELATIVE angle (driving only)
    if (nav.heading_valid && fabsf(nav.arrow_deg) > BLINK_DEG) {
        draw_blinker(nav.arrow_deg > 0 ? 1 : -1, fabsf(nav.arrow_deg) > 90.0f, phase);
    }

    // right column, clear of the ring
    fmt_miles(nav.distance_m, dist, sizeof(dist));
    int w = (int)strlen(dist) * 8 * 4;
    rlcd_draw_text(RLCD_W - w - 10, 92, dist, 4, false);
    fmt_age(st.partner.age_s, age, sizeof(age));
    snprintf(buf, sizeof(buf), "age %s", age);
    rlcd_draw_text(RLCD_W - (int)strlen(buf) * 16 - 10, 132, buf, 2, false);
    if (nav.heading_valid) {
        rlcd_draw_text(216, 170, "needle = YOU", 1, false);
        rlcd_draw_text(216, 186, "dart   = PARTNER", 1, false);
    } else {
        rlcd_draw_text(RLCD_W - 7 * 16 - 10, 166, "stopped", 2, false);
    }

    // priority banners
    if (!st.ble_connected)                     banner(28, "RADIO LINK LOST");
    else if (st.partner.age_s > STALE_AGE_S)   banner(28, "PARTNER DATA STALE");
    else if (warn)
        banner(28, nav.arrow_deg > 0 ? "CHANGE COURSE >>" : "<< CHANGE COURSE");

    snprintf(buf, sizeof(buf), "link %s - tap:info hold:reset",
             st.ble_connected ? "OK" : "LOST");
    rlcd_draw_text(8, 288, buf, 1, false);
}

static void render_status(const TrackerState &st, const NavOutput &nav) {
    char buf[48], age[12], dist[16];
    rlcd_clear(true);
    ctext(8, "OVERALL TRACKER", 2, false);
    ctext(42, st.ble_connected ? "LINK CONNECTED" : "LINK SEARCHING...", 2, false);

    if (st.self.valid) {
        snprintf(buf, sizeof(buf), "ME  %.5f %.5f", st.self.lat_deg, st.self.lon_deg);
        ctext(80, buf, 2, false);
        fmt_age(st.self.age_s, age, sizeof(age));
        snprintf(buf, sizeof(buf), "spd %.0f mph - age %s", st.self.speed_mps * 2.23694f, age);
        ctext(104, buf, 2, false);
    } else {
        ctext(80, "ME  waiting for GPS fix", 2, false);
    }

    if (st.partner.valid) {
        snprintf(buf, sizeof(buf), "PTR %.5f %.5f", st.partner.lat_deg, st.partner.lon_deg);
        ctext(142, buf, 2, false);
        fmt_age(st.partner.age_s, age, sizeof(age));
        snprintf(buf, sizeof(buf), "age %s", age);
        ctext(166, buf, 2, false);
    } else {
        ctext(142, "PTR no partner heard yet", 2, false);
    }

    if (nav.valid) {
        fmt_miles(nav.distance_m, dist, sizeof(dist));
        ctext(200, dist, 5, false);
        snprintf(buf, sizeof(buf), "PARTNER IS %s OF YOU", cardinal8(nav.bearing_deg));
        ctext(250, buf, 2, false);
    }
    rlcd_draw_text(8, 282, "tap:compass hold:reset", 1, false);
}

static void render_searching(const TrackerState &st) {
    char buf[48];
    rlcd_clear(true);
    ctext(96, "SEARCHING FOR PARTNER", 2, false);
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

    for (;;) {
        // KEY: tap = page toggle, hold ~1 s = tracking reset
        if (digitalRead(TRACK_RESET_PIN) == LOW) {
            if (++held == 2) { node_table_reset(); flash_ticks = 4; }
        } else {
            if (held == 1) s_page ^= 1; // released after a short tap
            held = 0;
        }

        TrackerState st;
        tracker_store_get(&st);
        NavOutput nav = nav_compute(&st);

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
            else if (s_page == 0)          render_nav(st, nav, warn, (tick & 1) == 0);
            else                           render_status(st, nav);
            if (flash_ticks > 0) {
                flash_ticks--;
                rlcd_fill_rect(0, 130, RLCD_W, 34, false);
                ctext(139, "TRACKING RESET", 2, true);
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
