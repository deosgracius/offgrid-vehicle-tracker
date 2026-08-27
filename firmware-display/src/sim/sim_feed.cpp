#include "sim_feed.h"
#include <math.h>
#include <string.h>

// Base location: Lubbock, TX (change freely — the math doesn't care).
static const double BASE_LAT = 33.5779;
static const double BASE_LON = -101.8552;
static const double M_PER_DEG_LAT = 111320.0;

static SimScenario s_sc;
static float s_t;          // sim time, seconds

static double m_per_deg_lon(double lat_deg) {
    return M_PER_DEG_LAT * cos(lat_deg * M_PI / 180.0);
}

void sim_feed_init(SimScenario sc) {
    s_sc = sc;
    s_t = 0.0f;
}

const char *sim_scenario_name(SimScenario sc) {
    static const char *names[SIM_SCENARIO_COUNT] = {
        "PARTNER_APPROACHING", "PARTNER_CROSSING", "STATIONARY", "STALE_DATA", "LINK_LOST"};
    return (sc < SIM_SCENARIO_COUNT) ? names[sc] : "?";
}

void sim_feed_tick(float dt_s, TrackerState *out) {
    s_t += dt_s;
    memset(out, 0, sizeof(*out));
    out->ble_connected = true;

    // Default self: driving due north at 20 m/s (~45 mph).
    out->self.valid = true;
    out->self.lat_deg = BASE_LAT + (20.0 * s_t) / M_PER_DEG_LAT;
    out->self.lon_deg = BASE_LON;
    out->self.course_deg = 0.0f;
    out->self.speed_mps = 20.0f;

    switch (s_sc) {
    case SIM_PARTNER_APPROACHING: {
        // Partner starts 5 km south-east, closes at 25 m/s on a NNW course.
        float closed = 25.0f * s_t;
        float remain = 5000.0f - closed;
        if (remain < 50.0f) remain = 50.0f;
        out->partner.valid = true;
        out->partner.lat_deg = out->self.lat_deg - (remain * 0.8) / M_PER_DEG_LAT;
        out->partner.lon_deg = BASE_LON + (remain * 0.6) / m_per_deg_lon(BASE_LAT);
        out->partner.course_deg = 340.0f;
        out->partner.speed_mps = 25.0f;
        out->partner.age_s = (uint32_t)fmodf(s_t, 30.0f); // fresh every 30 s broadcast
        break;
    }
    case SIM_PARTNER_CROSSING: {
        // Partner 1 km ahead, moving west->east at 15 m/s.
        out->partner.valid = true;
        out->partner.lat_deg = out->self.lat_deg + 1000.0 / M_PER_DEG_LAT;
        out->partner.lon_deg = BASE_LON + ((-2000.0 + 15.0 * s_t)) / m_per_deg_lon(BASE_LAT);
        out->partner.course_deg = 90.0f;
        out->partner.speed_mps = 15.0f;
        out->partner.age_s = (uint32_t)fmodf(s_t, 30.0f);
        break;
    }
    case SIM_STATIONARY:
        out->self.speed_mps = 0.0f;   // heading invalid -> compass-rose mode
        out->self.lat_deg = BASE_LAT;
        out->partner.valid = true;
        out->partner.lat_deg = BASE_LAT + 2000.0 / M_PER_DEG_LAT;
        out->partner.lon_deg = BASE_LON + 2000.0 / m_per_deg_lon(BASE_LAT);
        out->partner.speed_mps = 0.0f;
        out->partner.age_s = (uint32_t)fmodf(s_t, 30.0f);
        break;
    case SIM_STALE_DATA:
        // Partner froze 3 km north 10 s in; age grows unbounded after that.
        out->partner.valid = true;
        out->partner.lat_deg = BASE_LAT + 3000.0 / M_PER_DEG_LAT;
        out->partner.lon_deg = BASE_LON;
        out->partner.age_s = (s_t > 10.0f) ? (uint32_t)(s_t - 10.0f) : 0;
        break;
    case SIM_LINK_LOST:
        out->partner.valid = true;
        out->partner.lat_deg = BASE_LAT + 2000.0 / M_PER_DEG_LAT;
        out->partner.lon_deg = BASE_LON;
        out->partner.age_s = 5;
        out->ble_connected = fmodf(s_t, 20.0f) < 12.0f; // drops 8 s of every 20 s
        break;
    default:
        break;
    }
}
