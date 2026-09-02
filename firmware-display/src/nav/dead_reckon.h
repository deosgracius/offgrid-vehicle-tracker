// Dead reckoning: project fixes forward along their last course/speed so the
// display feels live between 10-60 s radio broadcasts. Owner: Deo.
//
// Honesty rules: age_s is NEVER touched (the driver still sees real data age,
// and the STALE banner still fires on it), and projection stops at
// DR_MAX_PROJECT_S - past that the estimate is fiction, so the fix freezes at
// its last projected point.
#pragma once
#include "tracker_state.h"

#define DR_MAX_PROJECT_S 120u   // matches the UI's STALE threshold

#ifdef __cplusplus
extern "C" {
#endif

// Project one fix forward by its own age (capped). No-op unless the fix is
// valid and was moving (speed > 0 - the parked deadband already zeroes noise).
void dr_project_fix(Fix *f);

// Project both fixes of a TrackerState in place. Call right after
// tracker_store_get(), before nav_compute() / rendering.
void dr_apply(TrackerState *st);

#ifdef __cplusplus
}
#endif
