#include "tracker_store.h"
#include <Arduino.h>
#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>
#include <string.h>

static TrackerState s_state;
static SemaphoreHandle_t s_mutex;

void tracker_store_init(void) {
    s_mutex = xSemaphoreCreateMutex();
    memset(&s_state, 0, sizeof(s_state));
}

void tracker_store_set(const TrackerState *st) {
    xSemaphoreTake(s_mutex, portMAX_DELAY);
    s_state = *st;
    xSemaphoreGive(s_mutex);
}

void tracker_store_get(TrackerState *out) {
    xSemaphoreTake(s_mutex, portMAX_DELAY);
    *out = s_state;
    xSemaphoreGive(s_mutex);
}
