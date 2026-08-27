// Meshtastic BLE client link. Owner: Deo. State machine per ARCHITECTURE.md §5.
//
// Meshtastic Client API over BLE (docs: meshtastic.org/docs/development/device/client-api):
//   Service   6ba1b218-15a8-461f-9fa8-5dcae273eafd
//   ToRadio   f75c76d2-129e-4dad-a1dd-7866124401e7   (write:  ToRadio protobufs)
//   FromRadio 8ba2bcc2-ee02-4a55-a531-c525c5e454d5   (read:   FromRadio protobufs, drain until empty)
//   FromNum   ed9da18c-a800-4f66-a670-aa7547e34453   (notify: "new data available" counter)
//
// Protocol: on connect, write ToRadio{want_config_id} -> node DB + MyNodeInfo stream in via
// FromRadio reads. Then each FromNum notify means "read FromRadio until it returns empty."
// Verify the whole API from a laptop first:  pip install meshtastic ; meshtastic --ble-scan
#pragma once

typedef enum {
    BLE_SCANNING,
    BLE_CONNECTING,
    BLE_BONDING,
    BLE_SUBSCRIBED,
    BLE_DRAINING,
} BleLinkState;

void ble_link_init(void);          // start NimBLE, load bond keys from NVS
void ble_link_task(void *arg);     // FreeRTOS task: runs the state machine forever
BleLinkState ble_link_state(void);
