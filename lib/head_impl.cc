/* -*- c++ -*- */
/*
 * Copyright 2023 gr-txid author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "head_impl.h"

namespace gr {
  namespace txid {

    head::sptr
    head::make(size_t sizeof_stream_item, uint64_t nitems, bool blocking)
    {
      return gnuradio::make_block_sptr<head_impl>(
        sizeof_stream_item, nitems, blocking);
    }


    /*
     * The private constructor
     */
    head_impl::head_impl(size_t sizeof_stream_item, uint64_t nitems, bool blocking)
      : gr::block("head",
              gr::io_signature::make(1, 1, sizeof(sizeof_stream_item)),
              gr::io_signature::make(1, 1, sizeof(sizeof_stream_item))),
              d_nitems(nitems), d_ncopied_items(0), d_blocking(blocking)
    {}

    /*
     * Our virtual destructor.
     */
    head_impl::~head_impl()
    {
    }

    int
    head_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      if(d_ncopied_items >= d_nitems){
        // if (!d_blocking) {
        //   return -1; // Done!
        // }
        consume_each(noutput_items);
        return 0;
      }
      unsigned n = std::min(d_nitems - d_ncopied_items,
                            (uint64_t)noutput_items);

      if(n == 0){
        if(!d_blocking)
          consume_each(noutput_items);
        return 0;
      }

      memcpy(output_items[0], input_items[0],
             n * input_signature()->sizeof_stream_item (0));
      d_ncopied_items += n;

      if (d_blocking) {
        consume_each(n);
      } else {
        consume_each(noutput_items);
      }
      return n;
    }

  } /* namespace txid */
} /* namespace gr */
