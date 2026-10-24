#include "nav.h"
#include <math.h>

#define EARTH_R_M 6371000.0
#define DEG2RAD(d) ((d) * (M_PI / 180.0))
#define RAD2DEG(r) ((r) * (180.0 / M_PI))

float nav_wrap360(float deg) {
    float d = fmodf(deg, 360.0f);
    if (d < 0.0f) d += 360.0f;
    return d;
}

float nav_wrap180(float deg) {
    float d = nav_wrap360(deg);
    if (d >= 180.0f) d -= 360.0f;
    return d;
}

float nav_haversine_m(double lat1_deg, double lon1_deg, double lat2_deg, double lon2_deg) {
    double p1 = DEG2RAD(lat1_deg), p2 = DEG2RAD(lat2_deg);
    double dp = DEG2RAD(lat2_deg - lat1_deg);
    double dl = DEG2RAD(lon2_deg - lon1_deg);
    double a = sin(dp / 2) * sin(dp / 2) + cos(p1) * cos(p2) * sin(dl / 2) * sin(dl / 2);
    double c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a));
    return (float)(EARTH_R_M * c);
}

float nav_initial_bearing_deg(double lat1_deg, double lon1_deg, double lat2_deg, double lon2_deg) {
    double p1 = DEG2RAD(lat1_deg), p2 = DEG2RAD(lat2_deg);
    double dl = DEG2RAD(lon2_deg - lon1_deg);
    double y = sin(dl) * cos(p2);
    double x = cos(p1) * sin(p2) - sin(p1) * cos(p2) * cos(dl);
    return nav_wrap360((float)RAD2DEG(atan2(y, x)));
}

static float s_held_course_deg = 0.0f;
static bool  s_has_held = false;

void nav_reset_heading(void) {
    s_has_held = false;
    s_held_course_deg = 0.0f;
}

NavOutput nav_compute(const TrackerState *st) {
    NavOutput out = {0};
    if (!st->self.valid || !st->partner.valid) {
        return out; // out.valid == false
    }
    out.valid = true;
    out.distance_m = nav_haversine_m(st->self.lat_deg, st->self.lon_deg,
                                     st->partner.lat_deg, st->partner.lon_deg);
    out.bearing_deg = nav_initial_bearing_deg(st->self.lat_deg, st->self.lon_deg,
                                              st->partner.lat_deg, st->partner.lon_deg);
    out.heading_valid = st->self.speed_mps >= NAV_MIN_HEADING_SPEED_MPS;
    if (out.heading_valid) {
        s_held_course_deg = st->self.course_deg;
        s_has_held = true;
    }
    out.heading_held = !out.heading_valid && s_has_held;
    float nose = s_has_held ? s_held_course_deg : 0.0f;  // never moved: north = 12
    out.arrow_deg = nav_wrap180(out.bearing_deg - nose);
    return out;
}
