/* -*- c++ -*- */
/*
 * Copyright 2023 Cyrille Morin.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/txid/packet_header_ofdm.h>
#include <gnuradio/digital/lfsr.h>
#include <gnuradio/io_signature.h>

namespace gr {
namespace txid {

int _get_header_len_from_occupied_carriers(
    const std::vector<std::vector<int>>& occupied_carriers, int n_syms)
{
    int header_len = 0;
    for (int i = 0; i < n_syms; i++) {
        header_len += occupied_carriers[i].size();
    }

    return header_len;
}

packet_header_ofdm::sptr
packet_header_ofdm::make(const std::vector<std::vector<int>>& occupied_carriers,
                            int n_syms,
                            const std::string& len_tag_key,
                            const std::string& frame_len_tag_key,
                            const std::string& num_tag_key,
                            int bits_per_header_sym,
                            int bits_per_payload_sym,
                            bool scramble_header,
                            int expected_len)
{
    return packet_header_ofdm::sptr(new packet_header_ofdm(occupied_carriers,
                                                                 n_syms,
                                                                 len_tag_key,
                                                                 frame_len_tag_key,
                                                                 num_tag_key,
                                                                 bits_per_header_sym,
                                                                 bits_per_payload_sym,
                                                                 scramble_header,
                                                                 expected_len));
}

packet_header_ofdm::packet_header_ofdm(
    const std::vector<std::vector<int>>& occupied_carriers,
    int n_syms,
    const std::string& len_key_name,
    const std::string& frame_key_name,
    const std::string& num_key_name,
    int bits_per_header_sym,
    int bits_per_payload_sym,
    bool scramble_header,
    int expected_len)
    : packet_header_default(
          _get_header_len_from_occupied_carriers(occupied_carriers, n_syms),
          len_key_name,
          num_key_name,
          bits_per_header_sym),
      d_frame_len_tag_key(pmt::string_to_symbol(frame_key_name)),
      d_occupied_carriers(occupied_carriers),
      d_bits_per_payload_sym(bits_per_payload_sym),
      d_scramble_mask(d_header_len, 0),
      d_expected_len(expected_len)
{
    d_crc_impl =
        gr::digital::crc(8, 0x07, 0xFF, 0x00, false, false);
    // Init scrambler mask
    if (scramble_header) {
        // These are just random values which already have OK PAPR:
        gr::digital::lfsr shift_reg(0x8a, 0x6f, 7);
        for (int i = 0; i < d_header_len; i++) {
            for (int k = 0; k < bits_per_header_sym; k++) {
                d_scramble_mask[i] ^= shift_reg.next_bit() << k;
            }
        }
    }
}

packet_header_ofdm::~packet_header_ofdm() {}

bool packet_header_ofdm::header_formatter(long packet_len,
                                             unsigned char* out,
                                             const std::vector<tag_t>& tags)
{
    packet_len &= 0xFFFF;
    unsigned char buffer[] = { (unsigned char)(packet_len & 0xFF),
                               (unsigned char)(packet_len >> 8),
                               (unsigned char)(d_header_number & 0xFF),
                               (unsigned char)(d_header_number >> 8),
                            };
    unsigned char crc = d_crc_impl.compute(buffer, sizeof(buffer));

    memset(out, 0x00, d_header_len);
    int k = 0; // Position in out
    for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
        out[k] = (unsigned char)((packet_len >> i) & d_mask);
    }
    for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
        out[k] = (unsigned char)((d_header_number >> i) & d_mask);
    }
    for (int i = 0; i < 8 && k < d_header_len; i += d_bits_per_byte, k++) {
        out[k] = (unsigned char)((crc >> i) & d_mask);
    }
    d_header_number++;
    d_header_number &= 0x0FFF;


    for (int i = 0; i < d_header_len; i++) {
        out[i] ^= d_scramble_mask[i];
    }
    return true;
}

bool packet_header_ofdm::header_parser(const unsigned char* in,
                                          std::vector<tag_t>& tags)
{
    std::vector<unsigned char> in_descrambled(d_header_len, 0);
    for (int i = 0; i < d_header_len; i++) {
        in_descrambled[i] = in[i] ^ d_scramble_mask[i];
    }

    unsigned packet_len = 0;
    unsigned header_num = 0;
    tag_t tag;

    // --------  Packet Length section  ---------
    int k = 0; // Position in "in"
    for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
        packet_len |= (((int)in_descrambled[k]) & d_mask) << i;
    }

    unsigned pack_len = packet_len;
    // Convert bytes to complex symbols:
    packet_len = packet_len * 8; // Convert to bits
    packet_len = packet_len / d_bits_per_payload_sym +
                 (int)(packet_len % d_bits_per_payload_sym > 0); // To cmplx symbols

    if (d_expected_len > 0 &&
        d_expected_len != pack_len) // Reject unexpected packet length
    {
        return false;
    }
    tag.key = d_len_tag_key;
    tag.value = pmt::from_long(packet_len);
    tags.push_back(tag);

    // To figure out how many payload OFDM symbols there are in this frame,
    // we need to go through the carrier allocation and count the number of
    // allocated carriers per OFDM symbol.
    // frame_len = # of payload OFDM symbols in this frame
    int frame_len = 0;
    size_t position = 0; // position in the carrier allocation map
    unsigned symbols_accounted_for = 0;
    while (symbols_accounted_for < packet_len) {
        frame_len++;
        symbols_accounted_for += d_occupied_carriers[position].size();
        position = (position + 1) % d_occupied_carriers.size();
    }
    tag.key = d_frame_len_tag_key;
    tag.value = pmt::from_long(frame_len);
    tags.push_back(tag);

    if (k >= d_header_len) { // Header too short to contain CRC, no verification
        return true;
    }

    // --------  Packet Number section  ---------
    if (d_num_tag_key == pmt::PMT_NIL) {
        k += 12;
    } else {
        for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
            header_num |= (((int)in_descrambled[k]) & d_mask) << i;
        }
        tag.key = d_num_tag_key;
        tag.value = pmt::from_long(header_num);
        tags.push_back(tag);
    }
    if (k >= d_header_len) { // Header too short to contain CRC, no verification
        return true;
    }

    // --------  CRC check section  ---------
    unsigned char buffer[] = { (unsigned char)(pack_len & 0xFF),
                               (unsigned char)(pack_len >> 8),
                               (unsigned char)(header_num & 0xFF),
                               (unsigned char)(header_num >> 8)};
    unsigned char crc_calcd = d_crc_impl.compute(buffer, sizeof(buffer));
    for (int i = 0; i < 8 && k < d_header_len; i += d_bits_per_byte, k++) {
        if ((((int)in_descrambled[k]) & d_mask) != (((int)crc_calcd >> i) & d_mask)) {
            return false;
        }
    }

    return true;
}

} /* namespace txid */
} /* namespace gr */
