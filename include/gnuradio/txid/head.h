/* -*- c++ -*- */
/*
 * Copyright 2023 gr-txid author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TXID_HEAD_H
#define INCLUDED_TXID_HEAD_H

#include <gnuradio/txid/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace txid {

    /*!
     * \brief <+description of block+>
     * \ingroup txid
     *
     */
    class TXID_API head : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<head> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of txid::head.
       *
       * To avoid accidental use of raw pointers, txid::head's
       * constructor is in a private implementation
       * class. txid::head::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t sizeof_stream_item, uint64_t nitems, bool blocking);
      virtual void reset() = 0;
      virtual void set_length(uint64_t nitems) = 0;
      virtual void set_blocking(bool blocking) = 0;
    };

  } // namespace txid
} // namespace gr

#endif /* INCLUDED_TXID_HEAD_H */
