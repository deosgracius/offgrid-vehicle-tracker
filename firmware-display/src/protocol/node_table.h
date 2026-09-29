// Tracks own + partner node fixes from decoded Meshtastic messages and
// publishes TrackerState. Owner: Deo.
#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

void node_table_init(void);
void node_table_set_self_num(uint32_t node_num);

// Called by proto_decode for every NodeInfo/User learned (config dump or live
// packet). Caches num->short_name; names may arrive before the node is
// selected as self/partner, so lookups happen at publish time.
void node_table_set_name(uint32_t node_num, const char *short_name);

// Called by proto_decode for every TEXT_MESSAGE_APP payload (raw UTF-8, not
// NUL-terminated). Messages from OUR OWN node are ignored (the radio echoes
// sent messages back over BLE; only the receiving display should notify).
// Kept as latest-message popup + a small history, published with a seq bump.
void node_table_text(uint32_t from_num, const uint8_t *text, size_t len);

// Driver "clear messages" (hold KEY on the messages page): empties the
// history and dismisses any active popup.
void node_table_clear_messages(void);

// Called by proto_decode for device telemetry: radio battery level
// (0..100, 101 = external power).
void node_table_battery(uint32_t from_num, uint32_t battery_level);

// Called by proto_decode for every position learned (live packet or config-dump
// snapshot). lat/lon in 1e-7 deg (Meshtastic wire format), track in 1e-5 deg,
// speed in km/h (converted to m/s internally). has_* mirror the proto flags.
void node_table_position(uint32_t from_num,
                         int32_t lat_i, int32_t lon_i, bool has_latlon,
                         uint32_t ground_track_1e5, bool has_track,
                         uint32_t ground_speed_kmh, bool has_speed,
                         uint32_t utc_epoch);  // 0 = packet carried no time

// Recompute ages and push TrackerState to the store. Call ~1 Hz.
void node_table_publish(bool ble_connected);

// Driver "tracking reset": discard current self+partner fixes; both re-acquire
// from the next live packets. Node identities are kept.
void node_table_reset(void);

uint32_t node_table_self_num(void);
uint32_t node_table_partner_num(void);
