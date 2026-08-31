// Location-aware local time (the recorded product requirement): GPS supplies
// UTC; the timezone is derived from the vehicle's position — no user setting.
// Zones covered: US Eastern/Central/Mountain/Pacific/Alaska by lon/lat bands
// (approximate political boundaries; good along road-trip corridors).
// DST window is approximated within a few days at the March/November edges.
#pragma once
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Formats e.g. "11:42a CDT". Returns false (out untouched) if epoch == 0.
bool local_time_fmt(uint32_t utc_epoch, double lat_deg, double lon_deg,
                    char *out, size_t olen);

#ifdef __cplusplus
}
#endif
