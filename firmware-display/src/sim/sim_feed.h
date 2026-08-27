// Simulated TrackerState feed — first-class dev tool, not a hack (ARCHITECTURE.md §3).
// Lets the whole UI + nav stack run with zero radios. Owner: shared (Josiah uses it daily).
#pragma once
#include "tracker_state.h"

typedef enum {
    SIM_PARTNER_APPROACHING,  // partner closes from 5 km behind-right while we drive N
    SIM_PARTNER_CROSSING,     // partner crosses left-to-right ahead of us
    SIM_STATIONARY,           // both stopped -> exercises compass-rose fallback
    SIM_STALE_DATA,           // partner packets stop -> age counts up
    SIM_LINK_LOST,            // BLE drops mid-drive -> UI link indicator
    SIM_SCENARIO_COUNT
} SimScenario;

void sim_feed_init(SimScenario sc);
// Advance the simulation by dt seconds and write the resulting state to *out.
void sim_feed_tick(float dt_s, TrackerState *out);
const char *sim_scenario_name(SimScenario sc);
