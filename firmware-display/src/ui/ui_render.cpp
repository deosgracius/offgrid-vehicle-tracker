#include "ui_render.h"
#include "../protocol/tracker_store.h"
#include "../nav/nav.h"
#include "rlcd.h"
#include <Arduino.h>
#include <stdio.h>

// DEBUG display — raw TrackerState on the RLCD so the protocol firmware is
// testable without a laptop. Deliberately plain text: the real driver UI
// (big rotating arrow, Fig. 4 of the overview PDF) is Josiah's — this file
// hands him a working driver (rlcd.h) and gets out of his way.

static bool s_have_panel = false;

void ui_render_init(void) {
    s_have_panel = rlcd_init();
    Serial.printf("[ui] RLCD init %s\n", s_have_panel ? "OK" : "FAILED (serial only)");
    if (s_have_panel) {
        rlcd_clear(true);
        rlcd_draw_text(24, 120, "GROUP 9 TRACKER", 3, false);
        rlcd_draw_text(24, 160, "protocol debug screen", 2, false);
        rlcd_flush();
    }
}

static void draw_line(int *y, const char *txt, int scale) {
    rlcd_draw_text(8, *y, txt, scale, false);
    *y += 8 * scale + 6;
}

static void render_panel(const TrackerState &st, const NavOutput &nav) {
    char buf[48];
    int y = 6;
    rlcd_clear(true);

    rlcd_draw_text(8, y, "GROUP 9 TRACKER", 2, false);
    y += 22;
    rlcd_fill_rect(8, y, RLCD_W - 16, 2, false); // divider
    y += 8;

    snprintf(buf, sizeof(buf), "LINK %s", st.ble_connected ? "CONNECTED" : "SEARCHING...");
    draw_line(&y, buf, 2);

    if (st.self.valid) {
        snprintf(buf, sizeof(buf), "ME  %.5f %.5f", st.self.lat_deg, st.self.lon_deg);
        draw_line(&y, buf, 2);
        snprintf(buf, sizeof(buf), "    spd %.0f m/s  age %lus",
                 st.self.speed_mps, (unsigned long)st.self.age_s);
        draw_line(&y, buf, 2);
    } else {
        draw_line(&y, "ME  waiting for GPS fix", 2);
    }

    if (st.partner.valid) {
        snprintf(buf, sizeof(buf), "PTR %.5f %.5f", st.partner.lat_deg, st.partner.lon_deg);
        draw_line(&y, buf, 2);
        snprintf(buf, sizeof(buf), "    age %lus", (unsigned long)st.partner.age_s);
        draw_line(&y, buf, 2);
    } else {
        draw_line(&y, "PTR no partner heard yet", 2);
    }

    y += 6;
    if (nav.valid) {
        if (nav.distance_m >= 1000.0f)
            snprintf(buf, sizeof(buf), "%.2f km", nav.distance_m / 1000.0f);
        else
            snprintf(buf, sizeof(buf), "%.0f m", nav.distance_m);
        rlcd_draw_text(8, y, buf, 4, false); // big distance
        y += 40;
        if (nav.heading_valid)
            snprintf(buf, sizeof(buf), "arrow %+.0f deg", nav.arrow_deg);
        else
            snprintf(buf, sizeof(buf), "bearing %.0f deg true", nav.bearing_deg);
        draw_line(&y, buf, 2);
    }

    snprintf(buf, sizeof(buf), "up %lus", (unsigned long)(millis() / 1000));
    rlcd_draw_text(8, RLCD_H - 20, buf, 1, false);
    rlcd_flush();
}

void ui_render_task(void *arg) {
    (void)arg;
    for (;;) {
        TrackerState st;
        tracker_store_get(&st);
        NavOutput nav = nav_compute(&st);

        if (s_have_panel) render_panel(st, nav);

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
