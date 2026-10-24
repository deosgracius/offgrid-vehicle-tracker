// Nav-math unit tests — run on your laptop, no hardware:  pio test -e native
#include <unity.h>
#include "../../src/nav/nav.h"
#include "../../src/nav/dead_reckon.h"

void setUp(void) { nav_reset_heading(); }
void tearDown(void) {}

static TrackerState make_state(double slat, double slon, float course, float speed,
                               double plat, double plon) {
    TrackerState st = {};
    st.self.valid = true;
    st.self.lat_deg = slat; st.self.lon_deg = slon;
    st.self.course_deg = course; st.self.speed_mps = speed;
    st.partner.valid = true;
    st.partner.lat_deg = plat; st.partner.lon_deg = plon;
    st.ble_connected = true;
    return st;
}

void test_one_degree_longitude_at_equator(void) {
    // 1 deg of arc on a 6371 km sphere = 111.19 km
    TEST_ASSERT_FLOAT_WITHIN(200.0f, 111195.0f, nav_haversine_m(0, 0, 0, 1));
}

void test_one_degree_latitude(void) {
    TEST_ASSERT_FLOAT_WITHIN(200.0f, 111195.0f, nav_haversine_m(0, 0, 1, 0));
}

void test_zero_distance(void) {
    TEST_ASSERT_FLOAT_WITHIN(0.5f, 0.0f, nav_haversine_m(33.5779, -101.8552, 33.5779, -101.8552));
}

void test_bearing_cardinals(void) {
    TEST_ASSERT_FLOAT_WITHIN(0.1f,   0.0f, nav_initial_bearing_deg(0, 0, 1, 0));   // north
    TEST_ASSERT_FLOAT_WITHIN(0.1f,  90.0f, nav_initial_bearing_deg(0, 0, 0, 1));   // east
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 180.0f, nav_initial_bearing_deg(1, 0, 0, 0));   // south
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 270.0f, nav_initial_bearing_deg(0, 1, 0, 0));   // west
}

void test_wrap(void) {
    TEST_ASSERT_FLOAT_WITHIN(0.01f,  10.0f, nav_wrap360(370.0f));
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 350.0f, nav_wrap360(-10.0f));
    TEST_ASSERT_FLOAT_WITHIN(0.01f, -10.0f, nav_wrap180(350.0f));
    TEST_ASSERT_FLOAT_WITHIN(0.01f, 100.0f, nav_wrap180(-260.0f));
}

void test_arrow_is_bearing_minus_course(void) {
    // Partner due east (bearing 90), we drive course 350 -> arrow +100 (right-rear)
    TrackerState st = make_state(0, 0, 350.0f, 20.0f, 0, 0.5);
    NavOutput nav = nav_compute(&st);
    TEST_ASSERT_TRUE(nav.valid);
    TEST_ASSERT_TRUE(nav.heading_valid);
    TEST_ASSERT_FLOAT_WITHIN(0.2f, 100.0f, nav.arrow_deg);
}

void test_slow_speed_falls_back_to_compass(void) {
    // Never moved this session: no live heading, no held heading, so the
    // nose is north and the arrow equals the absolute bearing.
    TrackerState st = make_state(0, 0, 123.0f, 1.0f /* < 2.2 m/s */, 1, 0);
    NavOutput nav = nav_compute(&st);
    TEST_ASSERT_TRUE(nav.valid);
    TEST_ASSERT_FALSE(nav.heading_valid);
    TEST_ASSERT_FALSE(nav.heading_held);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, nav.bearing_deg); // partner due north
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, nav.arrow_deg);   // 12 o'clock = north
}

void test_stopped_holds_last_course(void) {
    // Drive course 350 with the partner due east (arrow +100), then stop:
    // the nose stays at 350 so the clock position does not jump.
    TrackerState st = make_state(0, 0, 350.0f, 20.0f, 0, 0.5);
    NavOutput moving = nav_compute(&st);
    TEST_ASSERT_TRUE(moving.heading_valid);
    st.self.speed_mps = 0.0f;
    st.self.course_deg = 77.0f;   // GPS course is noise when parked; must be ignored
    NavOutput parked = nav_compute(&st);
    TEST_ASSERT_FALSE(parked.heading_valid);
    TEST_ASSERT_TRUE(parked.heading_held);
    TEST_ASSERT_FLOAT_WITHIN(0.2f, 100.0f, parked.arrow_deg);
}

void test_invalid_fix_gives_invalid_output(void) {
    TrackerState st = make_state(0, 0, 0, 20.0f, 1, 1);
    st.partner.valid = false;
    NavOutput nav = nav_compute(&st);
    TEST_ASSERT_FALSE(nav.valid);
}

void test_dr_projects_north(void) {
    // 10 m/s due north for 10 s = 100 m = ~0.000899 deg lat, lon unchanged
    Fix f = {}; f.valid = true; f.lat_deg = 33.0; f.lon_deg = -101.0;
    f.course_deg = 0.0f; f.speed_mps = 10.0f; f.age_s = 10;
    dr_project_fix(&f);
    TEST_ASSERT_FLOAT_WITHIN(0.5f, 100.0f, nav_haversine_m(33.0, -101.0, f.lat_deg, f.lon_deg));
    TEST_ASSERT_TRUE(f.lon_deg == -101.0);  // exactly untouched
    TEST_ASSERT_TRUE(f.lat_deg > 33.0);
    TEST_ASSERT_EQUAL_UINT32(10, f.age_s); // age must be untouched
}

void test_dr_projects_east_scales_by_latitude(void) {
    // Due east at 20 m/s for 30 s = 600 m along the 33N parallel
    Fix f = {}; f.valid = true; f.lat_deg = 33.0; f.lon_deg = -101.0;
    f.course_deg = 90.0f; f.speed_mps = 20.0f; f.age_s = 30;
    dr_project_fix(&f);
    TEST_ASSERT_FLOAT_WITHIN(3.0f, 600.0f, nav_haversine_m(33.0, -101.0, f.lat_deg, f.lon_deg));
    TEST_ASSERT_TRUE(f.lat_deg == 33.0);  // exactly untouched
    TEST_ASSERT_TRUE(f.lon_deg > -101.0);
}

void test_dr_parked_and_fresh_are_noops(void) {
    Fix parked = {}; parked.valid = true; parked.lat_deg = 33.0; parked.lon_deg = -101.0;
    parked.speed_mps = 0.0f; parked.age_s = 60;
    dr_project_fix(&parked);
    TEST_ASSERT_TRUE(parked.lat_deg == 33.0 && parked.lon_deg == -101.0);

    Fix fresh = {}; fresh.valid = true; fresh.lat_deg = 33.0; fresh.lon_deg = -101.0;
    fresh.course_deg = 45.0f; fresh.speed_mps = 20.0f; fresh.age_s = 0;
    dr_project_fix(&fresh);
    TEST_ASSERT_TRUE(fresh.lat_deg == 33.0 && fresh.lon_deg == -101.0);
}

void test_dr_caps_at_stale_horizon(void) {
    // 10 min old: projection must clamp to DR_MAX_PROJECT_S worth of travel
    Fix f = {}; f.valid = true; f.lat_deg = 33.0; f.lon_deg = -101.0;
    f.course_deg = 0.0f; f.speed_mps = 30.0f; f.age_s = 600;
    dr_project_fix(&f);
    TEST_ASSERT_FLOAT_WITHIN(20.0f, 30.0f * DR_MAX_PROJECT_S,
        nav_haversine_m(33.0, -101.0, f.lat_deg, f.lon_deg));
}

int main(int, char **) {
    UNITY_BEGIN();
    RUN_TEST(test_dr_projects_north);
    RUN_TEST(test_dr_projects_east_scales_by_latitude);
    RUN_TEST(test_dr_parked_and_fresh_are_noops);
    RUN_TEST(test_dr_caps_at_stale_horizon);
    RUN_TEST(test_one_degree_longitude_at_equator);
    RUN_TEST(test_one_degree_latitude);
    RUN_TEST(test_zero_distance);
    RUN_TEST(test_bearing_cardinals);
    RUN_TEST(test_wrap);
    RUN_TEST(test_arrow_is_bearing_minus_course);
    RUN_TEST(test_slow_speed_falls_back_to_compass);
    RUN_TEST(test_stopped_holds_last_course);
    RUN_TEST(test_invalid_fix_gives_invalid_output);
    return UNITY_END();
}
