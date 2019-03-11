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


#ifndef INCLUDED_TXID_HEAD_H
#define INCLUDED_TXID_HEAD_H

#include <txid/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace txid {

    /*!
     * \brief <+description of block+>
     * \ingroup learning
     *
     */
    class TXID_API head : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<head> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of learning::head.
       *
       * To avoid accidental use of raw pointers, learning::head's
       * constructor is in a private implementation
       * class. learning::head::make is the public interface for
       * creating new instances.
       */
       static sptr make(size_t sizeof_stream_item,
                        uint64_t nitems,
                      bool blocking);

      virtual void reset() = 0;
      virtual void set_length(uint64_t nitems) = 0;
      virtual void set_blocking(bool blocking) = 0;
    };

  } // namespace learning
} // namespace gr

#endif /* INCLUDED_LEARNING_HEAD_H */
