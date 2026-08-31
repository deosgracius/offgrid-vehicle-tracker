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
static const char *FROMRADIO_UUID = "2c55e69e-4993-11ed-b878-0242ac120002"; // fw 2.x UUID (old 8ba2bcc2-... is pre-2.x)
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
    void onDisconnect(NimBLEClient *c, int reason) override {
        Serial.printf("[ble] disconnected (reason %d)\n", reason);
        s_disconnected = true;
    }
    void onPassKeyEntry(NimBLEConnInfo &connInfo) override {
        Serial.println("[ble] passkey requested -> sending fixed PIN");
        NimBLEDevice::injectPassKey(connInfo, PAIRING_PIN);
    }
    void onConfirmPasskey(NimBLEConnInfo &connInfo, uint32_t pin) override {
        Serial.printf("[ble] confirm PIN %06lu\n", (unsigned long)pin);
        NimBLEDevice::injectConfirmPasskey(connInfo, pin == PAIRING_PIN);
    }
    void onAuthenticationComplete(NimBLEConnInfo &connInfo) override {
        Serial.printf("[ble] auth complete: encrypted=%d bonded=%d\n",
                      connInfo.isEncrypted(), connInfo.isBonded());
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
    // Heltec runs bluetooth.mode FIXED_PIN (123456): passkey-entry pairing.
    // We are the keyboard side; onPassKeyEntry injects the PIN.
    NimBLEDevice::setSecurityAuth(/*bond*/ true, /*mitm*/ true, /*sc*/ true);
    NimBLEDevice::setSecurityIOCap(BLE_HS_IO_KEYBOARD_ONLY);
    NimBLEDevice::setMTU(517);
    NimBLEDevice::setPower(9); // +9 dBm — default TX is marginal for connect handshakes
    // NOTE: never deleteAllBonds() here — after a successful bond the Meshtastic
    // peripheral advertises for its bonded peer; wiping our keys at boot makes
    // it permanently unreachable until the peripheral is factory reset.
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

static bool try_connect(const NimBLEAddress &addr) {
    s_state = BLE_CONNECTING;
    s_client = NimBLEDevice::createClient();
    s_client->setClientCallbacks(&s_cb, false);
    s_client->setConnectTimeout(10000);
    bool connected = false;
    for (int attempt = 1; attempt <= 3 && !connected; attempt++) {
        connected = s_client->connect(addr);
        if (!connected) {
            Serial.printf("[ble] connect attempt %d failed\n", attempt);
            vTaskDelay(pdMS_TO_TICKS(250));
        }
    }
    if (!connected) return false;

    s_state = BLE_BONDING;
    if (!s_client->secureConnection()) {
        Serial.println("[ble] bonding failed (wrong PIN / rejected?)");
        return false;
    }

    NimBLERemoteService *svc = s_client->getService(SVC_UUID);
    if (!svc) { Serial.println("[ble] no Meshtastic service?!"); return false; }
    const std::vector<NimBLERemoteCharacteristic *> &chars = svc->getCharacteristics(true);
    Serial.printf("[ble] service has %u characteristics:\n", (unsigned)chars.size());
    for (auto *c : chars) Serial.printf("[ble]   %s\n", c->getUUID().toString().c_str());
    s_toRadio   = svc->getCharacteristic(TORADIO_UUID);
    s_fromRadio = svc->getCharacteristic(FROMRADIO_UUID);
    s_fromNum   = svc->getCharacteristic(FROMNUM_UUID);
    if (!s_toRadio || !s_fromRadio || !s_fromNum) {
        Serial.printf("[ble] missing characteristic(s): to=%d from=%d num=%d\n",
                      s_toRadio != nullptr, s_fromRadio != nullptr, s_fromNum != nullptr);
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
            static NimBLEAddress s_known_addr;
            static bool s_have_addr = false;

            bool attempt_now = false;
            if (s_have_addr) {
                // Known radio: skip scanning, fire directly. The connect itself
                // waits up to 10 s for an advertisement from that address, so
                // this is also our fastest way to catch a brief adv window.
                attempt_now = true;
            } else {
                NimBLEScan *scan = NimBLEDevice::getScan();
                scan->setActiveScan(true);
                NimBLEScanResults results = scan->getResults(1500, false);
                for (int i = 0; i < results.getCount(); i++) {
                    const NimBLEAdvertisedDevice *dev = results.getDevice(i);
                    if (dev->isAdvertisingService(NimBLEUUID(SVC_UUID))) {
                        s_known_addr = dev->getAddress();
                        s_have_addr = true;
                        attempt_now = true;
                        Serial.printf("[ble] found %s (%s) rssi %d\n",
                                      dev->getName().c_str(),
                                      s_known_addr.toString().c_str(),
                                      dev->getRSSI());
                        break;
                    }
                }
                scan->clearResults();
            }

            if (attempt_now) {
                if (!try_connect(s_known_addr)) {
                    teardown();
                    Serial.printf("[ble] retry in %d s\n", backoff_s);
                    vTaskDelay(pdMS_TO_TICKS(backoff_s * 1000));
                    if (backoff_s < 8) backoff_s *= 2;
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
