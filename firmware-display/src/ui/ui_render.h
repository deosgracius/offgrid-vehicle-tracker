// Display rendering. Owner: Josiah.
// Consumes TrackerState (via tracker_store_get) + nav_compute. Nothing else.
#pragma once

void ui_render_init(void);      // bring up RLCD panel + framebuffer (PSRAM)
void ui_render_task(void *arg); // FreeRTOS task: 1 Hz redraw loop
