/* -*- c++ -*- */
/*
 * Copyright 2023 gr-txid author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TXID_CORRELATOR_IMPL_H
#define INCLUDED_TXID_CORRELATOR_IMPL_H

#include <gnuradio/txid/correlator.h>
#include <gnuradio/filter/fft_filter.h>
using namespace gr::filter;
namespace gr {
  namespace txid {

    class correlator_impl : public correlator
    {
     private:
      pmt::pmt_t d_src_id;
      std::vector<gr_complex> d_symbols;
      const float d_sps;
      unsigned int d_mark_delay, d_stashed_mark_delay;
      float d_thresh, d_stashed_threshold;
      kernel::fft_filter_ccc d_filter;

      volk::vector<gr_complex> d_corr;
      volk::vector<float> d_corr_mag;
      volk::vector<float> d_mag;

      float d_power;
      float d_scale;
      float d_pfa; // probability of false alarm

      const tm_type d_threshold_method;

      void _set_mark_delay(unsigned int mark_delay);
      void _set_threshold(float threshold);

      static constexpr int s_nitems = 24 * 1024;

     public:
      correlator_impl(const std::vector<gr_complex>& symbols,
                      float sps,
                      unsigned int mark_delay,
                      float threshold = 0.9,
                      tm_type threshold_method = THRESHOLD_ABSOLUTE);
      ~correlator_impl() override;

      std::vector<gr_complex> symbols() const override;
      void set_symbols(const std::vector<gr_complex>& symbols) override;

      unsigned int mark_delay() const override;
      void set_mark_delay(unsigned int mark_delay) override;

      float threshold() const override;
      void set_threshold(float threshold) override;

      int work(int noutput_items,
              gr_vector_const_void_star& input_items,
              gr_vector_void_star& output_items) override;
    };

  } // namespace txid
} // namespace gr

#endif /* INCLUDED_TXID_CORRELATOR_IMPL_H */
