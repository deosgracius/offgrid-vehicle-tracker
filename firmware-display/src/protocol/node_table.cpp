#include "node_table.h"
#include "tracker_store.h"
#include <Arduino.h>
#include <string.h>

// Partner selection (bring-up rule): first non-self node heard becomes the
// partner. TODO(Deo): persist a chosen partner node ID in NVS + UI selection.

typedef struct {
    Fix      fix;
    uint32_t last_update_ms;  // millis() of last NEW fix; 0 = never
    // Raw wire values of the last accepted fix, for re-broadcast detection:
    // a radio with no GPS lock re-sends its last known position every cycle,
    // bit-identical. A live fix always jitters in the low digits, so an exact
    // repeat means "no new measurement" and must NOT reset the data age.
    int32_t  raw_lat_i, raw_lon_i;
    uint32_t raw_trk, raw_spd;
} Entry;

static uint32_t s_self_num;
static uint32_t s_partner_num;
static Entry s_self, s_partner;
static uint32_t s_utc_epoch;   // latest GPS wall-clock seen in any packet
static uint32_t s_utc_ref_ms;

// num -> short_name cache. Names can arrive (config dump) before we know which
// node becomes self/partner, so keep the last few and look up at publish time.
#define NAME_CACHE_N 6
typedef struct { uint32_t num; char name[TRACKER_NAME_LEN]; } NameEntry;
static NameEntry s_names[NAME_CACHE_N];
static int s_name_next;

void node_table_set_name(uint32_t node_num, const char *short_name) {
    if (node_num == 0 || short_name == NULL || short_name[0] == '\0') return;
    for (int i = 0; i < NAME_CACHE_N; i++) {
        if (s_names[i].num == node_num) {
            strncpy(s_names[i].name, short_name, TRACKER_NAME_LEN - 1);
            return;
        }
    }
    NameEntry *e = &s_names[s_name_next];
    s_name_next = (s_name_next + 1) % NAME_CACHE_N;
    e->num = node_num;
    memset(e->name, 0, sizeof(e->name));
    strncpy(e->name, short_name, TRACKER_NAME_LEN - 1);
    Serial.printf("[node] name 0x%08lx = '%s'\n", (unsigned long)node_num, e->name);
}

static const char *lookup_name(uint32_t node_num) {
    if (node_num != 0)
        for (int i = 0; i < NAME_CACHE_N; i++)
            if (s_names[i].num == node_num) return s_names[i].name;
    return "";
}

void node_table_init(void) {
    s_self_num = s_partner_num = 0;
    memset(&s_self, 0, sizeof(s_self));
    memset(&s_partner, 0, sizeof(s_partner));
    memset(s_names, 0, sizeof(s_names));
    s_name_next = 0;
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
                         uint32_t ground_speed_kmh, bool has_speed,
                         uint32_t utc_epoch) {
    if (utc_epoch > 1600000000UL &&        // sanity: after 2020 => real GPS time
        utc_epoch >= s_utc_epoch) {        // monotonic: a stale re-broadcast may
        s_utc_epoch = utc_epoch;           // carry the old fix time - never let
        s_utc_ref_ms = millis();           // the clock run backwards
    }
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

    if (e->fix.valid && lat_i == e->raw_lat_i && lon_i == e->raw_lon_i &&
        ground_track_1e5 == e->raw_trk && ground_speed_kmh == e->raw_spd) {
        // Exact repeat of the previous fix: the radio has no new measurement
        // and is re-broadcasting the old one. Keep the age counting so the
        // driver sees honest staleness (and the STALE banner past 120 s).
        Serial.printf("[node] dup pos 0x%08lx - stale rebroadcast, age keeps counting\n",
                      (unsigned long)from_num);
        return;
    }
    e->raw_lat_i = lat_i;
    e->raw_lon_i = lon_i;
    e->raw_trk = ground_track_1e5;
    e->raw_spd = ground_speed_kmh;
    e->fix.lat_deg = lat_i * 1e-7;
    e->fix.lon_deg = lon_i * 1e-7;
    if (has_track) e->fix.course_deg = ground_track_1e5 * 1e-5f;
    if (has_speed) {
        // Wire unit is km/h (mesh.proto: "Ground speed in km/h"), integer.
        // Deadband first: a parked GPS with a poor sky view reports its
        // position jitter as 1-3 km/h of phantom speed; <4.5 zeroes that and
        // keeps it from flipping the compass into heading-up mode.
        float kmh = (float)ground_speed_kmh;
        e->fix.speed_mps = (kmh < 4.5f) ? 0.0f : kmh / 3.6f;
    }
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

void node_table_reset(void) {
    memset(&s_self, 0, sizeof(s_self));
    memset(&s_partner, 0, sizeof(s_partner));
    Serial.println("[node] tracking reset - reacquiring fixes");
}

void node_table_publish(bool ble_connected) {
    refresh_age(&s_self);
    refresh_age(&s_partner);
    TrackerState st;
    memset(&st, 0, sizeof(st));
    st.self = s_self.fix;
    st.partner = s_partner.fix;
    st.ble_connected = ble_connected;
    st.utc_epoch = s_utc_epoch;
    st.utc_ref_ms = s_utc_ref_ms;
    strncpy(st.self_name, lookup_name(s_self_num), TRACKER_NAME_LEN - 1);
    strncpy(st.partner_name, lookup_name(s_partner_num), TRACKER_NAME_LEN - 1);
    tracker_store_set(&st);
}
