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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <pmt/pmt.h>
#include "packet_isolator_c_impl.h"

namespace gr {
  namespace txid {

    packet_isolator_c::sptr
    packet_isolator_c::make(int payload_length, int preamble_length, int lookup_window, char* tag_name)
    {
      return gnuradio::get_initial_sptr
      (new packet_isolator_c_impl(payload_length, preamble_length, lookup_window, tag_name));
    }

    /*
    * The private constructor
    */
    packet_isolator_c_impl::packet_isolator_c_impl(int payload_length, int preamble_length, int lookup_window, char* tag_name)
    : gr::block("packet_isolator_c",
    gr::io_signature::make(1, 1, sizeof(gr_complex)),
    gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      d_transmit_preamble = 0;
      d_packet_number = 0;
      last_transmitted_offset = 0;
      d_payload_length = payload_length;
      d_preamble_length = preamble_length;
      d_lookup_window = lookup_window;
      d_pack_length = (d_transmit_preamble * d_preamble_length) + d_payload_length; //=d_payload_length if d_transmit_preamble=0
      d_tag_name = tag_name;
      d_transmit_from_last_call = 0;
      set_tag_propagation_policy(TPP_DONT);
      set_min_noutput_items(d_pack_length *5);
      set_output_multiple(d_pack_length*5);
    }

    /*
    * Our virtual destructor.
    */
    packet_isolator_c_impl::~packet_isolator_c_impl()
    {
    }

    void
    packet_isolator_c_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = int(noutput_items);
    }

    int
    packet_isolator_c_impl::general_work (int noutput_items,
      gr_vector_int &ninput_items, //Does not include the history?
      gr_vector_const_void_star &input_items,
      gr_vector_void_star &output_items)
      {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        read = nitems_read(0);
        max_offset = read + ninput_items[0]; //Offset corresponding to the last sample of the input array

        //We don't want to start looking at tags if we can't compare them in the lookup window
        max_tag_offset = max_offset  - d_lookup_window;

        written = nitems_written(0);
        output_number = 0; //Number of samples we are outputting


        std::vector<tag_t> tags;
        get_tags_in_range(tags, 0, read, max_offset, pmt::intern(d_tag_name));

        //printf("%s %d\n", "To transmit", d_transmit_from_last_call);
        int tags_considered = 0;
        if(d_transmit_from_last_call<=noutput_items){
          memcpy(out, in, d_transmit_from_last_call * sizeof(gr_complex));
          output_number += d_transmit_from_last_call;
        }
        else{
          // printf("%s\n", "Something went wrong: there is not enough output space to finish transferring packet");
        }



        for(int i=0; i < tags.size();i++){
          if(tags[i].offset > max_tag_offset){ //Just in case
            d_transmit_from_last_call = 0;
            break;
          }

          if(tags[i].offset > d_relevant_tag.offset + d_lookup_window){
            d_relevant_tag = tags[i];
          }
          for(int j =i + 1; j < tags.size();j++){
            if(tags[j].offset > d_relevant_tag.offset + d_lookup_window){
              break;
            }

            if (pmt::to_double(d_relevant_tag.value) < pmt::to_double(tags[j].value)){
              d_relevant_tag = tags[j];
            }
            i++;
          }

          if(d_relevant_tag.offset <= last_transmitted_offset + d_lookup_window){
            // printf("%s %lu %lu\n", "We wanted to transmit twice this offset:", last_transmitted_offset + d_lookup_window, d_relevant_tag.offset);
            continue;
          }

          // if(d_relevant_tag.offset > last_transmitted_offset + d_lookup_window+3000){
          //   printf("%s %d\n", "We probably skipped a packet: diff=", d_relevant_tag.offset-last_transmitted_offset);
          //
          // }else{
          //   printf("%s %d\n", "We probably NOT!!!!! skipped a packet: diff=", d_relevant_tag.offset-last_transmitted_offset);
          // }

          position = d_relevant_tag.offset - read; //Position of the tag relative to the input array

          //Write a tag at the beginning of the payload
          tag_offset = written + d_transmit_from_last_call + tags_considered*d_pack_length + (d_preamble_length*d_transmit_preamble);


          if(position + d_preamble_length+d_payload_length > ninput_items[0]){ //Do we have enough room to read all the packet samples?
            to_transmit = ninput_items[0] - position;
            add_item_tag(0, written + d_transmit_from_last_call + tags_considered*d_pack_length + to_transmit, pmt::intern("transmission_halted"), pmt::mp(d_relevant_tag.offset));
            consume_each(position); //We consume every item up to the relevant tag offset
            return output_number;
          }else{
            to_transmit = d_pack_length;
          }
          if (position+to_transmit>=ninput_items[0]) {
            // printf("%s %d\n", "Something went wrong! ", position+to_transmit - ninput_items[0]);
          }
          //Forward a slice of inputs
          memcpy(out + d_transmit_from_last_call + tags_considered*d_pack_length, in + position+(d_preamble_length*(!d_transmit_preamble)), to_transmit * sizeof(gr_complex));
          d_transmit_from_last_call = d_pack_length - to_transmit;


          //Custom tag propagation scheme.
          std::vector<tag_t> tags_to_propagate;
          get_tags_in_range(tags_to_propagate, 0, d_relevant_tag.offset + (d_preamble_length*(!d_transmit_preamble)), d_relevant_tag.offset + d_preamble_length + d_payload_length);
          for(int index=0; index<tags_to_propagate.size(); index++){
            tag_offset = written + d_transmit_from_last_call + tags_considered*d_pack_length + (tags_to_propagate[index].offset - read - position);
            add_item_tag(0, tag_offset, tags_to_propagate[index].key, tags_to_propagate[index].value, tags_to_propagate[index].srcid);
          }

          output_number += to_transmit;
          if (output_number > noutput_items){ //We don't want to write more than the size of the output array
            // printf("%s\n", "This is relevant!");
            consume_each(position); //We consume every item up to the relevant tag offset
            return output_number - to_transmit;
          }
          add_item_tag(0, tag_offset+150, pmt::intern("header_start"), pmt::mp(d_packet_number++));

          tags_considered ++;
          last_transmitted_offset = d_relevant_tag.offset;
          if (to_transmit<d_pack_length) {
            break;
          }
        }


      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(ninput_items[0]);
      // Tell runtime system how many output items we produced.
      return output_number;
    }

  } /* namespace learning */
} /* namespace gr */
