// Meshtastic protobuf encode/decode (nanopb). Owner: Deo.
#pragma once
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

// Decode one FromRadio frame (one BLE read) and feed node_table.
// Returns false on parse failure (logged, not fatal).
bool proto_decode_from_radio(const uint8_t *buf, size_t len);

// Encode ToRadio{want_config_id: nonce}. Returns bytes written, 0 on error.
size_t proto_encode_want_config(uint8_t *buf, size_t buflen, uint32_t nonce);

// True once the config dump matching the nonce has completed.
bool proto_config_complete(void);
void proto_reset_config_state(void);
