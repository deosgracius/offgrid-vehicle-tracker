// Meshtastic BLE client — NimBLE central. Owner: Deo.
// State machine per docs/ARCHITECTURE.md §5. Verified against a real device via
// the Meshtastic Python CLI before this was written (W1 bench session).
#include "ble_link.h"
#include "node_table.h"
#include "proto_decode.h"
#include <Arduino.h>
#include <NimBLEDevice.h>

// Meshtastic Client API GATT UUIDs (see ble_link.h for the protocol notes).
static const char *SVC_UUID       = "6ba1b218-15a8-461f-9fa8-5dcae273eafd";
static const char *TORADIO_UUID   = "f75c76d2-129e-4dad-a1dd-7866124401e7";
static const char *FROMRADIO_UUID = "8ba2bcc2-ee02-4a55-a531-c525c5e454d5";
static const char *FROMNUM_UUID   = "ed9da18c-a800-4f66-a670-aa7547e34453";

// Our Heltec uses bluetooth.fixed_pin (confirmed via `meshtastic --get bluetooth`).
static const uint32_t PAIRING_PIN = 123456;

static volatile BleLinkState s_state = BLE_SCANNING;
static volatile bool s_notify_pending = false;
static volatile bool s_disconnected = false;

static NimBLEClient *s_client;
static NimBLERemoteCharacteristic *s_toRadio, *s_fromRadio, *s_fromNum;

BleLinkState ble_link_state(void) { return s_state; }

class ClientCallbacks : public NimBLEClientCallbacks {
    void onConnect(NimBLEClient *c) override {
        Serial.println("[ble] connected");
    }
    void onDisconnect(NimBLEClient *c) override {
        Serial.println("[ble] disconnected");
        s_disconnected = true;
    }
    uint32_t onPassKeyRequest() override {
        Serial.println("[ble] passkey requested -> sending fixed PIN");
        return PAIRING_PIN;
    }
    bool onConfirmPIN(uint32_t pin) override {
        Serial.printf("[ble] confirm PIN %06lu\n", (unsigned long)pin);
        return pin == PAIRING_PIN;
    }
    void onAuthenticationComplete(ble_gap_conn_desc *desc) override {
        Serial.printf("[ble] auth complete: encrypted=%d bonded=%d\n",
                      desc->sec_state.encrypted, desc->sec_state.bonded);
    }
};
static ClientCallbacks s_cb;

static void notify_cb(NimBLERemoteCharacteristic *chr, uint8_t *data,
                      size_t len, bool isNotify) {
    // FromNum notify = "new FromRadio data queued". Drain from the task, never here.
    s_notify_pending = true;
}

void ble_link_init(void) {
    node_table_init();
    NimBLEDevice::init("");
    NimBLEDevice::setSecurityAuth(/*bond*/ true, /*mitm*/ true, /*sc*/ true);
    NimBLEDevice::setSecurityIOCap(BLE_HS_IO_KEYBOARD_ONLY); // we type the PIN
    NimBLEDevice::setMTU(517);
    Serial.println("[ble] init done, scanning for Meshtastic service");
}

// Read FromRadio until it returns empty; feed every frame to the decoder.
static void drain_from_radio(void) {
    s_state = BLE_DRAINING;
    for (;;) {
        NimBLEAttValue v = s_fromRadio->readValue();
        if (v.size() == 0) break;
        proto_decode_from_radio(v.data(), v.size());
    }
    s_state = BLE_SUBSCRIBED;
}

static bool try_connect(const NimBLEAdvertisedDevice *dev) {
    s_state = BLE_CONNECTING;
    s_client = NimBLEDevice::createClient();
    s_client->setClientCallbacks(&s_cb, false);
    s_client->setConnectTimeout(10);
    if (!s_client->connect(const_cast<NimBLEAdvertisedDevice *>(dev))) {
        Serial.println("[ble] connect failed");
        return false;
    }

    s_state = BLE_BONDING;
    if (!s_client->secureConnection()) {
        Serial.println("[ble] bonding failed (wrong PIN / rejected?)");
        return false;
    }

    NimBLERemoteService *svc = s_client->getService(SVC_UUID);
    if (!svc) { Serial.println("[ble] no Meshtastic service?!"); return false; }
    s_toRadio   = svc->getCharacteristic(TORADIO_UUID);
    s_fromRadio = svc->getCharacteristic(FROMRADIO_UUID);
    s_fromNum   = svc->getCharacteristic(FROMNUM_UUID);
    if (!s_toRadio || !s_fromRadio || !s_fromNum) {
        Serial.println("[ble] missing characteristic(s)");
        return false;
    }
    if (!s_fromNum->subscribe(true, notify_cb)) {
        Serial.println("[ble] fromNum subscribe failed");
        return false;
    }
    s_state = BLE_SUBSCRIBED;

    // Handshake: ask for the config + node DB dump.
    uint8_t buf[32];
    uint32_t nonce = (uint32_t)esp_random();
    size_t n = proto_encode_want_config(buf, sizeof(buf), nonce);
    if (n == 0 || !s_toRadio->writeValue(buf, n, /*response*/ true)) {
        Serial.println("[ble] want_config write failed");
        return false;
    }
    Serial.printf("[ble] want_config sent (nonce %08lx), draining...\n",
                  (unsigned long)nonce);
    drain_from_radio();
    return true;
}

static void teardown(void) {
    if (s_client) {
        NimBLEDevice::deleteClient(s_client); // also disconnects
        s_client = nullptr;
    }
    s_toRadio = s_fromRadio = s_fromNum = nullptr;
    s_disconnected = false;
    s_notify_pending = false;
    proto_reset_config_state();
    s_state = BLE_SCANNING;
}

void ble_link_task(void *arg) {
    (void)arg;
    uint32_t last_publish_ms = 0;
    int backoff_s = 1;

    for (;;) {
        if (s_state == BLE_SCANNING) {
            node_table_publish(false);
            NimBLEScan *scan = NimBLEDevice::getScan();
            scan->setActiveScan(true);
            NimBLEScanResults results = scan->start(5, false);
            const NimBLEAdvertisedDevice *found = nullptr;
            for (int i = 0; i < results.getCount(); i++) {
                NimBLEAdvertisedDevice dev = results.getDevice(i);
                if (dev.isAdvertisingService(NimBLEUUID(SVC_UUID))) {
                    Serial.printf("[ble] found %s (%s) rssi %d\n",
                                  dev.getName().c_str(),
                                  dev.getAddress().toString().c_str(),
                                  dev.getRSSI());
                    found = new NimBLEAdvertisedDevice(dev);
                    break;
                }
            }
            scan->clearResults();
            if (found) {
                bool ok = try_connect(found);
                delete found;
                if (!ok) {
                    teardown();
                    Serial.printf("[ble] retry in %d s\n", backoff_s);
                    vTaskDelay(pdMS_TO_TICKS(backoff_s * 1000));
                    if (backoff_s < 30) backoff_s *= 2;
                } else {
                    backoff_s = 1;
                }
            }
            continue;
        }

        // Connected states -----------------------------------------------
        if (s_disconnected) {
            teardown();
            continue;
        }
        if (s_notify_pending) {
            s_notify_pending = false;
            drain_from_radio();
        }
        uint32_t now = millis();
        if (now - last_publish_ms >= 1000) {
            last_publish_ms = now;
            node_table_publish(true);
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}
