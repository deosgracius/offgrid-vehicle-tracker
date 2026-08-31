#include "local_time.h"
#include <stdio.h>

// Civil date from days since 1970-01-01 (Howard Hinnant's algorithm).
static void civil_from_days(int64_t z, int *y, int *m, int *d) {
    z += 719468;
    int64_t era = (z >= 0 ? z : z - 146096) / 146097;
    int64_t doe = z - era * 146097;
    int64_t yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    int64_t yy = yoe + era * 400;
    int64_t doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    int64_t mp = (5 * doy + 2) / 153;
    *d = (int)(doy - (153 * mp + 2) / 5 + 1);
    *m = (int)(mp < 10 ? mp + 3 : mp - 9);
    *y = (int)(yy + (*m <= 2));
}

// US DST: 2nd Sunday of March .. 1st Sunday of November (approximated:
// exact within a few days at the boundaries; fine for a dashboard clock).
static bool us_dst(int m, int d) {
    if (m > 3 && m < 11) return true;
    if (m == 3)  return d >= 14;
    if (m == 11) return false;
    return false;
}

// Standard-time UTC offset + abbreviations by rough US political bands.
static int zone_offset(double lat, double lon, const char **std_ab, const char **dst_ab) {
    if (lat > 51.0 && lon < -129.0) { *std_ab = "AKST"; *dst_ab = "AKDT"; return -9; }
    if (lon >= -85.0)               { *std_ab = "EST";  *dst_ab = "EDT";  return -5; }
    if (lon >= -97.5)               { *std_ab = "CST";  *dst_ab = "CDT";  return -6; }
    if (lon >= -111.0)              { *std_ab = "MST";  *dst_ab = "MDT";  return -7; }
    if (lon >= -129.0)              { *std_ab = "PST";  *dst_ab = "PDT";  return -8; }
    *std_ab = "AKST"; *dst_ab = "AKDT"; return -9;
}

bool local_time_fmt(uint32_t utc_epoch, double lat, double lon,
                    char *out, size_t olen) {
    if (utc_epoch == 0) return false;
    const char *std_ab, *dst_ab;
    int off = zone_offset(lat, lon, &std_ab, &dst_ab);

    // First pass with standard offset to get the date, then apply DST.
    int64_t local = (int64_t)utc_epoch + (int64_t)off * 3600;
    int y, m, d;
    civil_from_days(local / 86400, &y, &m, &d);
    bool dst = us_dst(m, d);
    if (dst) {
        local += 3600;
        civil_from_days(local / 86400, &y, &m, &d);
    }
    int secs = (int)(local % 86400);
    if (secs < 0) secs += 86400;
    int hh = secs / 3600, mm = (secs % 3600) / 60;
    int h12 = hh % 12; if (h12 == 0) h12 = 12;
    snprintf(out, olen, "%d:%02d%c %s", h12, mm, hh < 12 ? 'a' : 'p',
             dst ? dst_ab : std_ab);
    return true;
}
