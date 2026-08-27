#include "ui_render.h"
#include "../protocol/tracker_store.h"
#include "../nav/nav.h"
#include <Arduino.h>

// TODO(Josiah): replace the Serial output with the RLCD driver from the
// Waveshare demo (github.com/waveshareteam/ESP32-S3-RLCD-4.2):
//   1. Panel init + full-screen framebuffer in PSRAM (300x400 / 8 = 15 KB mono).
//   2. Big rotating arrow (triangle rotated by arrow_deg; compass rose with an
//      absolute-bearing arrow when !heading_valid).
//   3. Distance readout, auto mi/km units; data age ("35 s ago"); link icon.
//   4. Screen layout per Fig. 4 of docs/Group9_Project_Overview.pdf.
// Until then this prints one status line per second — the full pipeline
// (store -> nav -> "render") is already exercised end to end.

void ui_render_init(void) {
    Serial.println("[ui] init (serial stub)");
}

void ui_render_task(void *arg) {
    (void)arg;
    for (;;) {
        TrackerState st;
        tracker_store_get(&st);
        NavOutput nav = nav_compute(&st);

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
