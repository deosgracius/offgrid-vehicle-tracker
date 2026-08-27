// Thread-safe holder of the shared TrackerState. Owner: Deo.
// One writer (protocol task), one reader (UI task) — see ARCHITECTURE.md §3.
#pragma once
#include "tracker_state.h"

void tracker_store_init(void);
void tracker_store_set(const TrackerState *st);   // protocol side ONLY
void tracker_store_get(TrackerState *out);        // UI side ONLY
