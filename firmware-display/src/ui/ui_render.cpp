#include "ui_render.h"
#include "../protocol/tracker_store.h"
#include "../nav/nav.h"
#include "rlcd.h"
#include <Arduino.h>
#include <stdio.h>
#include <math.h>

// Driver display, first pass (Fig. 4 of docs/Group9_Project_Overview.pdf):
// big rotated arrow + distance + data age + link status. Owner: Josiah —
// this is scaffolding for his lane; layout/polish/night-mode are his to shape.

static bool s_have_panel = false;

void ui_render_init(void) {
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

static void fill_triangle(float x0, float y0, float x1, float y1,
                          float x2, float y2, bool white) {
    int minx = (int)floorf(fminf(x0, fminf(x1, x2)));
    int maxx = (int)ceilf(fmaxf(x0, fmaxf(x1, x2)));
    int miny = (int)floorf(fminf(y0, fminf(y1, y2)));
    int maxy = (int)ceilf(fmaxf(y0, fmaxf(y1, y2)));
    float area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0);
    if (fabsf(area) < 0.01f) return;
    for (int y = miny; y <= maxy; y++) {
        for (int x = minx; x <= maxx; x++) {
            float w0 = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0);
            float w1 = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1);
            float w2 = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2);
            bool inside = (w0 >= 0 && w1 >= 0 && w2 >= 0) ||
                          (w0 <= 0 && w1 <= 0 && w2 <= 0);
            if (inside) rlcd_set_pixel(x, y, white);
        }
    }
}

// Arrow pointing "up" at deg=0, clockwise-positive (matches arrow_deg).
static void draw_arrow(int cx, int cy, float R, float deg) {
    float a = deg * (float)M_PI / 180.0f;
    float ca = cosf(a), sa = sinf(a);
    // Fig-4 style dart: tip, right barb, tail notch, left barb (local coords, y up)
    const float px[4] = {0.0f,  0.58f * R, 0.0f,      -0.58f * R};
    const float py[4] = {R,    -0.62f * R, -0.28f * R, -0.62f * R};
    float sx[4], sy[4];
    for (int i = 0; i < 4; i++) {
        // rotate (x,y) by deg clockwise, then flip y for screen coords
        float rx = px[i] * ca + py[i] * sa;
        float ry = -px[i] * sa + py[i] * ca;
        sx[i] = cx + rx;
        sy[i] = cy - ry;
    }
    fill_triangle(sx[0], sy[0], sx[1], sy[1], sx[2], sy[2], false);
    fill_triangle(sx[0], sy[0], sx[2], sy[2], sx[3], sy[3], false);
}

static void fmt_distance(float m, char *num, size_t nlen, const char **unit) {
    float mi = m / 1609.344f;
    if (mi >= 0.15f) {
        snprintf(num, nlen, mi >= 10.0f ? "%.0f" : "%.1f", mi);
        *unit = "miles";
    } else {
        snprintf(num, nlen, "%.0f", m * 3.28084f);
        *unit = "feet";
    }
}

static void fmt_age(uint32_t s, char *out, size_t olen) {
    if (s < 60)        snprintf(out, olen, "%lus", (unsigned long)s);
    else if (s < 3600) snprintf(out, olen, "%lum", (unsigned long)(s / 60));
    else               snprintf(out, olen, "%luh", (unsigned long)(s / 3600));
}

// ---- screens ---------------------------------------------------------------

static void render_tracking(const TrackerState &st, const NavOutput &nav) {
    char buf[48], num[12], age[12];
    const char *unit;
    rlcd_clear(true);

    rlcd_draw_text(144, 8, "PARTNER", 2, false);

    float arrow = nav.heading_valid ? nav.arrow_deg : nav.bearing_deg;
    draw_arrow(105, 150, 78.0f, arrow);
    if (!nav.heading_valid) {
        rlcd_draw_text(88, 236, "north up", 1, false); // stationary: no heading
    }

    fmt_distance(nav.distance_m, num, sizeof(num), &unit);
    int digits = strlen(num);
    int scale = digits <= 3 ? 6 : 5;
    rlcd_draw_text(212, 108, num, scale, false);
    rlcd_draw_text(212, 108 + 8 * scale + 8, unit, 2, false);

    fmt_age(st.partner.age_s, age, sizeof(age));
    snprintf(buf, sizeof(buf), "updated %s ago - link %s",
             age, st.ble_connected ? "OK" : "LOST");
    rlcd_draw_text(8, 278, buf, 2, false);
}

static void render_searching(const TrackerState &st) {
    char buf[48];
    rlcd_clear(true);
    rlcd_draw_text(32, 96, "SEARCHING FOR PARTNER", 2, false);
    snprintf(buf, sizeof(buf), "radio link: %s",
             st.ble_connected ? "connected" : "connecting...");
    rlcd_draw_text(32, 140, buf, 2, false);
    snprintf(buf, sizeof(buf), "own GPS:    %s",
             st.self.valid ? "locked" : "acquiring...");
    rlcd_draw_text(32, 168, buf, 2, false);
}

void ui_render_task(void *arg) {
    (void)arg;
    char up[16];
    for (;;) {
        TrackerState st;
        tracker_store_get(&st);
        NavOutput nav = nav_compute(&st);

        if (s_have_panel) {
            if (nav.valid) render_tracking(st, nav);
            else           render_searching(st);
            snprintf(up, sizeof(up), "up %lus", (unsigned long)(millis() / 1000));
            rlcd_draw_text(RLCD_W - 8 * (int)strlen(up) - 4, 2, up, 1, false);
            rlcd_flush();
        }

        if (!nav.valid) {
            Serial.printf("[ui] waiting for fix   ble=%d\n", st.ble_connected);
        } else if (nav.heading_valid) {
            Serial.printf("[ui] arrow %+7.1f deg  dist %8.0f m  age %4lus  ble=%d\n",
                          nav.arrow_deg, nav.distance_m,
                          (unsigned long)st.partner.age_s, st.ble_connected);
        } else {
            Serial.printf("[ui] compass %6.1f degT dist %8.0f m  age %4lus  ble=%d (rose mode)\n",
                          nav.bearing_deg, nav.distance_m,
                          (unsigned long)st.partner.age_s, st.ble_connected);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
