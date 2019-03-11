/* -*- c++ -*- */
/*
 * Copyright 2018 gr-learning author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "head_impl.h"

namespace gr {
  namespace txid {

    head::sptr
    head::make(size_t sizeof_stream_item, uint64_t nitems, bool blocking)
    {
      return gnuradio::get_initial_sptr
        (new head_impl(sizeof_stream_item, nitems, blocking));
    }

    /*
     * The private constructor
     */
    head_impl::head_impl(size_t sizeof_stream_item, uint64_t nitems, bool blocking)
      : gr::block("head",
              gr::io_signature::make(1, 1, sizeof_stream_item),
              gr::io_signature::make(1, 1, sizeof_stream_item)),
              d_nitems(nitems), d_ncopied_items(0), d_blocking(blocking)
    {}

    /*
     * Our virtual destructor.
     */
    head_impl::~head_impl()
    {
    }

    int
    head_impl::general_work(int noutput_items,
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

  } /* namespace learning */
} /* namespace gr */
