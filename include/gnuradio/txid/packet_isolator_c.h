/* -*- c++ -*- */
/*
 * Copyright 2023 Cyrille Morin.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TXID_PACKET_ISOLATOR_C_H
#define INCLUDED_TXID_PACKET_ISOLATOR_C_H

#include <gnuradio/txid/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace txid {

    /*!
     * \brief <+description of block+>
     * \ingroup txid
     *
     */
    class TXID_API packet_isolator_c : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<packet_isolator_c> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of txid::packet_isolator_c.
       *
       * To avoid accidental use of raw pointers, txid::packet_isolator_c's
       * constructor is in a private implementation
       * class. txid::packet_isolator_c::make is the public interface for
       * creating new instances.
       */
      static sptr make(int payload_length=0, int preamble_length = 80, int lookup_window = 30, std::string tag_name = "corr_est");
    };

  } // namespace txid
} // namespace gr

#endif /* INCLUDED_TXID_PACKET_ISOLATOR_C_H */
