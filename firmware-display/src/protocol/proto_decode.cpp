#include "proto_decode.h"
#include "node_table.h"
#include <Arduino.h>
#include <pb_decode.h>
#include <pb_encode.h>
#include "meshtastic/mesh.pb.h"

static uint32_t s_want_config_nonce;
static bool s_config_complete;

bool proto_config_complete(void) { return s_config_complete; }
void proto_reset_config_state(void) { s_config_complete = false; }

static void handle_position(uint32_t from_num, const meshtastic_Position *pos) {
    node_table_position(from_num,
                        pos->latitude_i, pos->longitude_i,
                        pos->has_latitude_i && pos->has_longitude_i,
                        pos->ground_track, pos->has_ground_track,
                        pos->ground_speed, pos->has_ground_speed,
                        pos->time);
}

static void handle_mesh_packet(const meshtastic_MeshPacket *pkt) {
    if (pkt->which_payload_variant != meshtastic_MeshPacket_decoded_tag) {
        return; // encrypted for someone else — not ours to read
    }
    const meshtastic_Data *data = &pkt->decoded;
    if (data->portnum == meshtastic_PortNum_POSITION_APP) {
        meshtastic_Position pos = meshtastic_Position_init_default;
        pb_istream_t is = pb_istream_from_buffer(data->payload.bytes, data->payload.size);
        if (pb_decode(&is, meshtastic_Position_fields, &pos)) {
            handle_position(pkt->from, &pos);
        } else {
            Serial.printf("[proto] Position decode failed: %s\n", PB_GET_ERROR(&is));
        }
    } else if (data->portnum == meshtastic_PortNum_NODEINFO_APP) {
        // Live node announcement: carries the User record (names + pubkey).
        meshtastic_User user = meshtastic_User_init_default;
        pb_istream_t is = pb_istream_from_buffer(data->payload.bytes, data->payload.size);
        if (pb_decode(&is, meshtastic_User_fields, &user)) {
            node_table_set_name(pkt->from, user.short_name);
        }
    }
    // Other portnums (TEXT_MESSAGE_APP, TELEMETRY_APP, ...) ignored for now.
}

bool proto_decode_from_radio(const uint8_t *buf, size_t len) {
    static meshtastic_FromRadio fr; // static: large struct, keep off task stack
    fr = (meshtastic_FromRadio)meshtastic_FromRadio_init_default;
    pb_istream_t is = pb_istream_from_buffer(buf, len);
    if (!pb_decode(&is, meshtastic_FromRadio_fields, &fr)) {
        Serial.printf("[proto] FromRadio decode failed (%u B): %s\n",
                      (unsigned)len, PB_GET_ERROR(&is));
        return false;
    }

    switch (fr.which_payload_variant) {
    case meshtastic_FromRadio_my_info_tag:
        node_table_set_self_num(fr.my_info.my_node_num);
        break;
    case meshtastic_FromRadio_node_info_tag: {
        const meshtastic_NodeInfo *ni = &fr.node_info;
        Serial.printf("[proto] node_info 0x%08lx '%s'\n",
                      (unsigned long)ni->num,
                      ni->has_user ? ni->user.long_name : "?");
        if (ni->has_user) node_table_set_name(ni->num, ni->user.short_name);
        if (ni->has_position) handle_position(ni->num, &ni->position);
        break;
    }
    case meshtastic_FromRadio_packet_tag:
        handle_mesh_packet(&fr.packet);
        break;
    case meshtastic_FromRadio_config_complete_id_tag:
        if (fr.config_complete_id == s_want_config_nonce) {
            s_config_complete = true;
            Serial.println("[proto] config dump complete");
        }
        break;
    default:
        break; // config, channels, metadata, ... — not needed yet
    }
    return true;
}

size_t proto_encode_position_request(uint8_t *buf, size_t buflen,
                                     uint32_t dest_num, uint32_t packet_id) {
    meshtastic_ToRadio tr = meshtastic_ToRadio_init_default;
    tr.which_payload_variant = meshtastic_ToRadio_packet_tag;
    meshtastic_MeshPacket *p = &tr.packet;
    p->to = dest_num;
    p->id = packet_id;          // nonzero so the mesh can dedupe retransmits
    p->channel = 0;             // primary channel (Group9) — channel-key encrypted
    p->hop_limit = 3;
    p->which_payload_variant = meshtastic_MeshPacket_decoded_tag;
    p->decoded.portnum = meshtastic_PortNum_POSITION_APP;
    p->decoded.want_response = true;  // peer's PositionModule replies with its fix
    p->decoded.payload.size = 0;      // empty Position — a pure request
    pb_ostream_t os = pb_ostream_from_buffer(buf, buflen);
    if (!pb_encode(&os, meshtastic_ToRadio_fields, &tr)) {
        Serial.printf("[proto] pos-request encode failed: %s\n", PB_GET_ERROR(&os));
        return 0;
    }
    return os.bytes_written;
}

size_t proto_encode_want_config(uint8_t *buf, size_t buflen, uint32_t nonce) {
    s_want_config_nonce = nonce;
    s_config_complete = false;
    meshtastic_ToRadio tr = meshtastic_ToRadio_init_default;
    tr.which_payload_variant = meshtastic_ToRadio_want_config_id_tag;
    tr.want_config_id = nonce;
    pb_ostream_t os = pb_ostream_from_buffer(buf, buflen);
    if (!pb_encode(&os, meshtastic_ToRadio_fields, &tr)) {
        Serial.printf("[proto] ToRadio encode failed: %s\n", PB_GET_ERROR(&os));
        return 0;
    }
    return os.bytes_written;
}
