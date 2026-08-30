#include "node_table.h"
#include "tracker_store.h"
#include <Arduino.h>
#include <string.h>

// Partner selection (bring-up rule): first non-self node heard becomes the
// partner. TODO(Deo): persist a chosen partner node ID in NVS + UI selection.

typedef struct {
    Fix      fix;
    uint32_t last_update_ms;  // millis() of last position update; 0 = never
} Entry;

static uint32_t s_self_num;
static uint32_t s_partner_num;
static Entry s_self, s_partner;

void node_table_init(void) {
    s_self_num = s_partner_num = 0;
    memset(&s_self, 0, sizeof(s_self));
    memset(&s_partner, 0, sizeof(s_partner));
}

void node_table_set_self_num(uint32_t node_num) {
    s_self_num = node_num;
    Serial.printf("[node] my node num: 0x%08lx\n", (unsigned long)node_num);
}

uint32_t node_table_self_num(void)    { return s_self_num; }
uint32_t node_table_partner_num(void) { return s_partner_num; }

void node_table_position(uint32_t from_num,
                         int32_t lat_i, int32_t lon_i, bool has_latlon,
                         uint32_t ground_track_1e5, bool has_track,
                         uint32_t ground_speed_mps, bool has_speed) {
    if (!has_latlon || (lat_i == 0 && lon_i == 0)) return; // no real fix

    Entry *e;
    if (from_num == s_self_num) {
        e = &s_self;
    } else {
        if (s_partner_num == 0) {
            s_partner_num = from_num;
            Serial.printf("[node] partner node: 0x%08lx\n", (unsigned long)from_num);
        }
        if (from_num != s_partner_num) return; // some third node — ignore for now
        e = &s_partner;
    }

    e->fix.lat_deg = lat_i * 1e-7;
    e->fix.lon_deg = lon_i * 1e-7;
    if (has_track) e->fix.course_deg = ground_track_1e5 * 1e-5f;
    if (has_speed) e->fix.speed_mps = (float)ground_speed_mps;
    e->fix.valid = true;
    e->last_update_ms = millis();

    Serial.printf("[node] pos 0x%08lx: %.6f, %.6f  spd %.1f  trk %.1f\n",
                  (unsigned long)from_num, e->fix.lat_deg, e->fix.lon_deg,
                  e->fix.speed_mps, e->fix.course_deg);
}

static void refresh_age(Entry *e) {
    if (e->fix.valid && e->last_update_ms != 0) {
        e->fix.age_s = (millis() - e->last_update_ms) / 1000UL;
    }
}

void node_table_publish(bool ble_connected) {
    refresh_age(&s_self);
    refresh_age(&s_partner);
    TrackerState st;
    st.self = s_self.fix;
    st.partner = s_partner.fix;
    st.ble_connected = ble_connected;
    tracker_store_set(&st);
}
