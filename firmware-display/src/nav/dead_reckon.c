#include "dead_reckon.h"
#include <math.h>

#define DR_M_PER_DEG_LAT 111320.0

void dr_project_fix(Fix *f) {
    if (!f->valid || f->speed_mps <= 0.0f) return;
    uint32_t dt = f->age_s;
    if (dt == 0) return;
    if (dt > DR_MAX_PROJECT_S) dt = DR_MAX_PROJECT_S;

    // Flat-earth step is plenty at these scales: worst case 120 s at highway
    // speed is ~4 km, where curvature error is centimeters.
    double c = f->course_deg * M_PI / 180.0;
    double d = (double)f->speed_mps * (double)dt;      // meters traveled
    double m_per_deg_lon = DR_M_PER_DEG_LAT * cos(f->lat_deg * M_PI / 180.0);
    if (m_per_deg_lon < 1.0) return;                   // polar guard
    f->lat_deg += (d * cos(c)) / DR_M_PER_DEG_LAT;
    f->lon_deg += (d * sin(c)) / m_per_deg_lon;
}

void dr_apply(TrackerState *st) {
    dr_project_fix(&st->self);
    dr_project_fix(&st->partner);
}
