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

#ifndef INCLUDED_TXID_HEAD_IMPL_H
#define INCLUDED_TXID_HEAD_IMPL_H

#include <txid/head.h>

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

      // Where all the action really happens
      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace learning
} // namespace gr

#endif /* INCLUDED_LEARNING_HEAD_IMPL_H */
