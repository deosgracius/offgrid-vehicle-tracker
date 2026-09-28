// Group 9 display-node firmware — entry point.
// SIM_MODE=1 (platformio.ini): simulator feeds TrackerState, no radios needed.
// SIM_MODE=0: Deo's BLE link feeds it from the Heltec.
#include <Arduino.h>
#include "protocol/tracker_store.h"
#include "protocol/ble_link.h"
#include "ui/ui_render.h"
#include "sim/sim_feed.h"

#if SIM_MODE
// BOOT button (GPIO0) cycles through the sim scenarios — live demo control.
#define SIM_BTN_PIN 0
static void sim_task(void *arg) {
    (void)arg;
    const float DT_S = 0.2f;
    TrackerState st;
    SimScenario cur = SIM_PARTNER_APPROACHING;
    pinMode(SIM_BTN_PIN, INPUT_PULLUP);
    bool was_down = false;
    for (;;) {
        bool down = digitalRead(SIM_BTN_PIN) == LOW;
        if (down && !was_down) {
            cur = (SimScenario)((cur + 1) % SIM_SCENARIO_COUNT);
            sim_feed_init(cur);
            Serial.printf("[sim] scenario -> %s\n", sim_scenario_name(cur));
        }
        was_down = down;
        sim_feed_tick(DT_S, &st);
        tracker_store_set(&st);
        vTaskDelay(pdMS_TO_TICKS((int)(DT_S * 1000)));
    }
}
#else
// BOOT button (GPIO0) in BLE mode = "request partner position": the radio
// sends a POSITION_APP want-response packet, the partner answers immediately
// instead of at its next scheduled broadcast. Useful when the partner is
// parked (60 s cadence) and you want its fix NOW.
#define POS_REQ_BTN_PIN 0
static void button_task(void *arg) {
    (void)arg;
    pinMode(POS_REQ_BTN_PIN, INPUT_PULLUP);
    bool was_down = false;
    for (;;) {
        bool down = digitalRead(POS_REQ_BTN_PIN) == LOW;
        if (down && !was_down) {
            Serial.println("[btn] request partner position");
            ble_link_request_partner_position();
        }
        was_down = down;
        vTaskDelay(pdMS_TO_TICKS(30)); // poll + debounce
    }
}
#endif

void setup() {
    Serial.begin(115200);
    delay(300);
    Serial.printf("\nGroup 9 tracker display — TrackerState v%d — %s\n",
                  TRACKER_STATE_VERSION, SIM_MODE ? "SIM_MODE" : "BLE mode");

    tracker_store_init();
    ui_render_init();

#if SIM_MODE
    sim_feed_init(SIM_PARTNER_APPROACHING);
    Serial.printf("[sim] scenario: %s\n", sim_scenario_name(SIM_PARTNER_APPROACHING));
    xTaskCreatePinnedToCore(sim_task, "sim", 4096, nullptr, 2, nullptr, 0);
#else
    ble_link_init();
    xTaskCreatePinnedToCore(ble_link_task, "ble", 8192, nullptr, 3, nullptr, 0);
    xTaskCreatePinnedToCore(button_task, "btn", 2048, nullptr, 2, nullptr, 0);
#endif
    xTaskCreatePinnedToCore(ui_render_task, "ui", 8192, nullptr, 1, nullptr, 1);
}

void loop() {
    vTaskDelay(pdMS_TO_TICKS(1000)); // everything lives in tasks
}
