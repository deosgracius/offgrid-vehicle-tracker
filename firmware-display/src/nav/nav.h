// Navigation math — pure functions, no hardware dependencies. Owner: Josiah.
// Unit-tested in test/test_nav (run: pio test -e native).
#pragma once
#include "tracker_state.h"

// Below this ground speed, GPS course-over-ground is noise; the UI must fall
// back to a north-referenced compass rose instead of a vehicle-relative arrow.
// 2.2 m/s ~= 5 mph.
#define NAV_MIN_HEADING_SPEED_MPS 2.2f

typedef struct {
    float distance_m;     // great-circle distance self -> partner
    float bearing_deg;    // true (north-referenced) initial bearing self -> partner, 0..360
    float arrow_deg;      // bearing relative to vehicle heading, -180..180 (0 = dead ahead)
    bool  heading_valid;  // false -> arrow_deg is meaningless; UI shows compass-rose mode
    bool  valid;          // false -> no usable pair of fixes; UI shows "waiting for fix"
} NavOutput;

#ifdef __cplusplus
extern "C" {
#endif

float nav_haversine_m(double lat1_deg, double lon1_deg, double lat2_deg, double lon2_deg);
float nav_initial_bearing_deg(double lat1_deg, double lon1_deg, double lat2_deg, double lon2_deg);
float nav_wrap360(float deg);   // -> [0, 360)
float nav_wrap180(float deg);   // -> [-180, 180)

// The one call the UI makes each frame.
NavOutput nav_compute(const TrackerState *st);

#ifdef __cplusplus
}
#endif
