/* -*- c++ -*- */
/*
 * Copyright 2023 Cyrille Morin.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TXID_PACKET_ISOLATOR_C_IMPL_H
#define INCLUDED_TXID_PACKET_ISOLATOR_C_IMPL_H

#include <gnuradio/txid/packet_isolator_c.h>

namespace gr {
  namespace txid {

    class packet_isolator_c_impl : public packet_isolator_c
    {
     private:
       int d_payload_length;
       int d_preamble_length;
       int d_lookup_window;
       int d_pack_length;
       int d_transmit_preamble;
       int d_transmit_from_last_call;
       int to_transmit;
       std::string d_tag_name;

       long d_packet_number;
       uint64_t read;
       long long history_read;
       uint64_t max_offset;

       uint64_t max_tag_offset;

       uint64_t written;
       int output_number;
       uint64_t position;
       uint64_t tag_offset;
       tag_t d_relevant_tag;
       uint64_t last_transmitted_offset;

     public:
      packet_isolator_c_impl(int payload_length, int preamble_length, int lookup_window, std::string tag_name);
      ~packet_isolator_c_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace txid
} // namespace gr

#endif /* INCLUDED_TXID_PACKET_ISOLATOR_C_IMPL_H */
