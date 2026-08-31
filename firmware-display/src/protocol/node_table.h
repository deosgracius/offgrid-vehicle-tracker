// Tracks own + partner node fixes from decoded Meshtastic messages and
// publishes TrackerState. Owner: Deo.
#pragma once
#include <stdint.h>
#include <stdbool.h>

void node_table_init(void);
void node_table_set_self_num(uint32_t node_num);

// Called by proto_decode for every position learned (live packet or config-dump
// snapshot). lat/lon in 1e-7 deg (Meshtastic wire format), track in 1e-5 deg,
// speed in m/s. has_* mirror the protobuf optional flags.
void node_table_position(uint32_t from_num,
                         int32_t lat_i, int32_t lon_i, bool has_latlon,
                         uint32_t ground_track_1e5, bool has_track,
                         uint32_t ground_speed_mps, bool has_speed);

// Recompute ages and push TrackerState to the store. Call ~1 Hz.
void node_table_publish(bool ble_connected);

// Driver "tracking reset": discard current self+partner fixes; both re-acquire
// from the next live packets. Node identities are kept.
void node_table_reset(void);

uint32_t node_table_self_num(void);
uint32_t node_table_partner_num(void);
