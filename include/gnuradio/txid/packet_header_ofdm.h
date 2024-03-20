/* -*- c++ -*- */
/*
 * Copyright 2023 Cyrille Morin.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TXID_PACKET_HEADER_OFDM_H
#define INCLUDED_TXID_PACKET_HEADER_OFDM_H

#include <gnuradio/txid/api.h>
#include <gnuradio/digital/packet_header_default.h>
#include <vector>

namespace gr {
namespace txid {

/*!
 * \brief Header utility for OFDM signals
 * \ingroup ofdm_blk
 */
class TXID_API packet_header_ofdm : public digital::packet_header_default
{
public:
    typedef std::shared_ptr<packet_header_ofdm> sptr;

    packet_header_ofdm(const std::vector<std::vector<int>>& occupied_carriers,
                          int n_syms,
                          const std::string& len_key_name,
                          const std::string& frame_key_name,
                          const std::string& num_key_name,
                          int bits_per_header_sym,
                          int bits_per_payload_sym,
                          bool scramble_header,
                          int expected_len);
    ~packet_header_ofdm() override;

    /*!
     * \brief Encodes the header information in the given tags into bits and places them
     * into \p out
     *
     * Uses the following header format:
     * Bits 0-11: The packet length (what was stored in the tag with key \p len_tag_key)
     * Bits 12-23: The header number (counts up everytime this function is called)
     * Bit 24-31: 8-Bit CRC
     * All other bits: Are set to zero
     *
     * If the header length is smaller than 40, bits are simply left out. For this
     * reason, they always start with the LSB.
     *
     * However, it is recommended to stay above 40 Bits, in order to have a working
     * CRC.
     * Also optionally scrambles the bits (this is more important for OFDM to avoid
     * PAPR spikes).
     */
    bool header_formatter(long packet_len,
                          unsigned char* out,
                          const std::vector<tag_t>& tags) override;

    /*!
     * \brief Inverse function to header_formatter().
     *
     * Does the same as packet_header_default::header_parser(), but
     * adds another tag that stores the number of OFDM symbols in the
     * packet, as well as the transmitter ID
     * Note that there is usually no linear connection between the number
     * of OFDM symbols and the packet length because a packet might
     * finish mid-OFDM-symbol.
     */
    bool header_parser(const unsigned char* header, std::vector<tag_t>& tags) override;

    /*!
     * \param occupied_carriers See carrier allocator
     * \param n_syms The number of OFDM symbols the header should be (usually 1)
     * \param len_tag_key The tag key used for the packet length (number of bytes)
     * \param frame_len_tag_key The tag key used for the frame length (number of
     *                          OFDM symbols, this is the tag key required for the
     *                          frame equalizer etc.)
     * \param num_tag_key The tag key used for packet numbering.
     * \param bits_per_header_sym Bits per complex symbol in the header, e.g. 1 if
     *                            the header is BPSK modulated, 2 if it's QPSK
     *                            modulated etc.
     * \param bits_per_payload_sym Bits per complex symbol in the payload. This is
     *                             required to figure out how many OFDM symbols
     *                             are necessary to encode the given number of
     *                             bytes.
     * \param scramble_header Set this to true to scramble the bits. This is highly
     *                        recommended, as it reduces PAPR spikes.
     * \param expected_len Expected packet length. Use -1 (default) if unkown. If set,
     * packet with a different length will be considered as invalid
     */
    static sptr make(const std::vector<std::vector<int>>& occupied_carriers,
                     int n_syms,
                     const std::string& len_tag_key = "packet_len",
                     const std::string& frame_len_tag_key = "frame_len",
                     const std::string& num_tag_key = "packet_num",
                     int bits_per_header_sym = 1,
                     int bits_per_payload_sym = 1,
                     bool scramble_header = false,
                     int expected_len = -1);


private:
    pmt::pmt_t d_frame_len_tag_key; //!< Tag key of the additional frame length tag
    const std::vector<std::vector<int>>
        d_occupied_carriers; //!< Which carriers/symbols carry data
    int d_bits_per_payload_sym;
    std::vector<unsigned char>
        d_scramble_mask; //!< Bits are xor'd with this before tx'ing
    int d_expected_len;
};

} // namespace txid
} // namespace gr

#endif /* INCLUDED_TXID_PACKET_HEADER_OFDM_H */
