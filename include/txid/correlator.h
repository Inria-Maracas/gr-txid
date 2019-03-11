/* -*- c++ -*- */
/*
 * Copyright 2018 Cyrille Morin.
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


#ifndef INCLUDED_TXID_CORRELATOR_H
#define INCLUDED_TXID_CORRELATOR_H

#include <txid/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace txid {

    /*!
     * \brief <+description of block+>
     * \ingroup learning
     *
     */
    class TXID_API correlator : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<correlator> sptr;

      enum tm_type {
        THRESHOLD_DYNAMIC,
        THRESHOLD_ABSOLUTE,
      };

      /*!
       * \brief Return a shared_ptr to a new instance of learning::correlator.
       *
       * To avoid accidental use of raw pointers, learning::correlator's
       * constructor is in a private implementation
       * class. learning::correlator::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::vector<gr_complex> &symbols, float sps, unsigned int mark_delay, float threshold = 0.9, tm_type threshold_method=THRESHOLD_ABSOLUTE);

      virtual std::vector<gr_complex> symbols() const = 0;
      virtual void set_symbols(const std::vector<gr_complex> &symbols) = 0;

      virtual unsigned int mark_delay() const = 0;
      virtual void set_mark_delay(unsigned int mark_delay) = 0;

      virtual float threshold() const = 0;
      virtual void set_threshold(float threshold) = 0;
    };

  } // namespace learning
} // namespace gr

#endif /* INCLUDED_LEARNING_CORRELATOR_H */
