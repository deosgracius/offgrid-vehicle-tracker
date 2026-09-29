// TrackerState — THE contract between protocol/ (Deo) and ui/+nav/ (Josiah).
// See docs/ARCHITECTURE.md §3. Pure data, no RTOS/Arduino dependencies, so it
// compiles on the native test environment too.
//
// Change policy: bump TRACKER_STATE_VERSION and update both sides in ONE commit,
// agreed by both owners.
#pragma once
#include <stdint.h>
#include <stdbool.h>

#define TRACKER_STATE_VERSION 3

// Meshtastic short names are up to 4 UTF-8 bytes; +1 for NUL, padded.
#define TRACKER_NAME_LEN 8

// One GPS fix. Angles in degrees, distances in meters, speeds in m/s.
typedef struct {
    double   lat_deg;
    double   lon_deg;
    float    course_deg;   // course over ground, 0..360, true north; meaningful only at speed
    float    speed_mps;    // ground speed
    uint32_t age_s;        // seconds since this fix was current (0 = fresh)
    bool     valid;        // false = never had a fix / fix lost long ago
} Fix;

typedef struct {
    Fix      self;          // own vehicle (from local Heltec's GPS via BLE)
    Fix      partner;       // partner vehicle (from mesh Position packets)
    bool     ble_connected; // in-cab link to our Heltec is up
    // Radio short names from NodeInfo (e.g. "SF", "RG"). Empty string = not
    // learned yet; UI falls back to generic ME/PTR labels.
    char     self_name[TRACKER_NAME_LEN];
    char     partner_name[TRACKER_NAME_LEN];
    // GPS wall-clock: UTC epoch seconds captured from the latest Position
    // packet, plus the local millis() when it was captured. Current UTC =
    // utc_epoch + (millis() - utc_ref_ms)/1000. 0 = no time received yet.
    uint32_t utc_epoch;
    uint32_t utc_ref_ms;
} TrackerState;
