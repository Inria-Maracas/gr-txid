/* -*- c++ -*- */
/*
 * Copyright 2023 gr-txid author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TXID_HEAD_IMPL_H
#define INCLUDED_TXID_HEAD_IMPL_H

#include <gnuradio/txid/head.h>

namespace gr {
  namespace txid {

    class head_impl : public head
    {
     private:
       uint64_t d_nitems;
       uint64_t d_ncopied_items;

       bool d_blocking;

     public:
      head_impl(size_t sizeof_stream_item, uint64_t nitems, bool blocking);
      ~head_impl();

      void reset() { d_ncopied_items = 0; }
      void set_length(uint64_t nitems) { d_nitems = nitems; }
      void set_blocking(bool blocking) { d_blocking = blocking; }

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace txid
} // namespace gr

#endif /* INCLUDED_TXID_HEAD_IMPL_H */
