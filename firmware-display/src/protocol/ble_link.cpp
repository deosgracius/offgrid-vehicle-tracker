#include "ble_link.h"
#include "tracker_store.h"
#include <Arduino.h>

// TODO(Deo): real implementation. Milestones, in order:
//   1. NimBLE central: scan for the Meshtastic service UUID, connect, bond
//      (PIN pairing once; NimBLE persists bond keys in NVS).
//   2. Write ToRadio{want_config_id=<nonce>} -> drain FromRadio: collect
//      MyNodeInfo (our node number) and NodeInfo for every known node.
//   3. Subscribe to FromNum notifications; on notify, drain FromRadio and feed
//      each buffer to proto_decode (nanopb) -> update node_table ->
//      tracker_store_set().
//   4. On disconnect: mark ble_connected=false in the store, back to scanning.
// Fallback decision point (W5): same protobufs over WiFi/TCP:4403 if BLE bonding
// proves hostile — only this file changes.

static volatile BleLinkState s_state = BLE_SCANNING;

BleLinkState ble_link_state(void) { return s_state; }

void ble_link_init(void) {
    Serial.println("[ble] init (stub) — SIM_MODE feeds the UI for now");
}

void ble_link_task(void *arg) {
    (void)arg;
    for (;;) {
        // Stub: report a disconnected link so the UI shows honest status if
        // anyone runs with SIM_MODE=0 before this is implemented.
        TrackerState st = {};
        st.ble_connected = false;
        tracker_store_set(&st);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
