// Nav-math unit tests — run on your laptop, no hardware:  pio test -e native
#include <unity.h>
#include "../../src/nav/nav.h"

void setUp(void) {}
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
    TrackerState st = make_state(0, 0, 123.0f, 1.0f /* < 2.2 m/s */, 1, 0);
    NavOutput nav = nav_compute(&st);
    TEST_ASSERT_TRUE(nav.valid);
    TEST_ASSERT_FALSE(nav.heading_valid);
    TEST_ASSERT_FLOAT_WITHIN(0.1f, 0.0f, nav.bearing_deg); // partner due north
}

void test_invalid_fix_gives_invalid_output(void) {
    TrackerState st = make_state(0, 0, 0, 20.0f, 1, 1);
    st.partner.valid = false;
    NavOutput nav = nav_compute(&st);
    TEST_ASSERT_FALSE(nav.valid);
}

int main(int, char **) {
    UNITY_BEGIN();
    RUN_TEST(test_one_degree_longitude_at_equator);
    RUN_TEST(test_one_degree_latitude);
    RUN_TEST(test_zero_distance);
    RUN_TEST(test_bearing_cardinals);
    RUN_TEST(test_wrap);
    RUN_TEST(test_arrow_is_bearing_minus_course);
    RUN_TEST(test_slow_speed_falls_back_to_compass);
    RUN_TEST(test_invalid_fix_gives_invalid_output);
    return UNITY_END();
}
