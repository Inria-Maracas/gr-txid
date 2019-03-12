#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Emitter
# Generated: Tue Dec 11 09:45:32 2018
##################################################

def struct(data): return type('Struct', (object,), data)()
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import learning
import numpy
import time


class emitter(gr.top_block):

    def __init__(self, gain_freq=2, is_random_source=0, max_gain=0.1, min_gain=0.001, nb_packets=70000, packet_len=400, port=3580, space_between_packets=200, tx_id=0, usrp_tx_gain=3, zeros_offset=100004, is_noise=0):
        gr.top_block.__init__(self, "Emitter")

        ##################################################
        # Parameters
        ##################################################
        self.gain_freq = gain_freq
        self.is_random_source = is_random_source
        self.max_gain = max_gain
        self.min_gain = min_gain
        self.nb_packets = nb_packets
        self.packet_len = packet_len
        self.port = port
        self.space_between_packets = space_between_packets
        self.tx_id = tx_id
        self.usrp_tx_gain = usrp_tx_gain
        self.zeros_offset = zeros_offset
        self.is_noise = is_noise

        ##################################################
        # Variables
        ##################################################
        self.preamble = preamble = (0, 1.00000000000000 + 0.00000000000000j, -0.0198821876650702 - 0.999802329770066j, 0.0596151251698190 + 0.998221436781933j, -0.992892073701974 + 0.119018191801903j, -0.980297366804636 + 0.197527397177953j, 0.293850274337919 + 0.955851461405761j, -0.405525320812986 - 0.914083811354038j, 0.848983362091364 - 0.528419578452620j, 0.754564620158230 - 0.656225749270376j, -0.780057308185211 - 0.625708075660561j, 0.888282612749130 + 0.459297289222982j, -0.255616632440464 + 0.966778225458040j, -0.0198821876650804 + 0.999802329770065j, 0.971669340040416 - 0.236344438532879j, -0.869320274439587 + 0.494249188616716j, -0.727878810369485 - 0.685705795086423j, -0.905840393665518 - 0.423619146408540j, -0.0992537989080696 + 0.995062150522427j, -0.255616632440477 - 0.966778225458036j, 0.804316565270771 - 0.594201028971703j, 0.511435479103437 - 0.859321680579653j, -0.992892073701971 - 0.119018191801923j, 0.949820131727787 - 0.312796607022213j, 0.700042074569421 + 0.714101599096754j, 0.949820131727768 + 0.312796607022273j, -0.177997895677522 - 0.984030867978426j, 0.641093637592130 + 0.767462668693983j, -0.331619278552096 + 0.943413299722125j, 0.216978808106213 + 0.976176314419074j, 0.700042074569433 - 0.714101599096743j, -0.177997895677626 + 0.984030867978407j, -0.905840393665558 + 0.423619146408453j, -0.476867501428628 + 0.878975190822367j, 0.987375341936355 - 0.158398024407083j, -0.671098428359002 + 0.741368261698650j, -0.999209397227295 - 0.0397565150970890j, -0.780057308185194 + 0.625708075660582j, 0.987375341936324 + 0.158398024407273j, -0.827304032543040 + 0.561754428320796j, -0.980297366804605 - 0.197527397178109j, -0.827304032543027 + 0.561754428320816j, 0.987375341936332 + 0.158398024407226j, -0.780057308185292 + 0.625708075660460j, -0.999209397227299 - 0.0397565150969950j, -0.671098428359083 + 0.741368261698577j, 0.987375341936350 - 0.158398024407110j, -0.476867501428484 + 0.878975190822446j, -0.905840393665478 + 0.423619146408624j, -0.177997895677642 + 0.984030867978404j, 0.700042074569508 - 0.714101599096669j, 0.216978808106132 + 0.976176314419092j, -0.331619278552151 + 0.943413299722105j, 0.641093637592190 + 0.767462668693933j, -0.177997895677511 - 0.984030867978428j, 0.949820131727754 + 0.312796607022316j, 0.700042074569284 + 0.714101599096888j, 0.949820131727893 - 0.312796607021891j, -0.992892073701961 - 0.119018191802010j, 0.511435479103736 - 0.859321680579474j, 0.804316565270626 - 0.594201028971898j, -0.255616632440350 - 0.966778225458070j, -0.0992537989081486 + 0.995062150522419j, -0.905840393665482 - 0.423619146408617j, -0.727878810369385 - 0.685705795086529j, -0.869320274439717 + 0.494249188616486j, 0.971669340040621 - 0.236344438532038j, -0.0198821876652695 + 0.999802329770062j, -0.255616632440926 + 0.966778225457918j, 0.888282612749188 + 0.459297289222869j, -0.780057308185057 - 0.625708075660753j, 0.754564620158670 - 0.656225749269870j, 0.848983362091728 - 0.528419578452034j, -0.405525320812299 - 0.914083811354343j, 0.293850274337947 + 0.955851461405753j, -0.980297366804665 + 0.197527397177809j, -0.992892073702018 + 0.119018191801536j, 0.0596151251691726 + 0.998221436781972j, -0.0198821876650031 - 0.999802329770067j, 1.00000000000000 + 4.46840285540623e-13j)
        self.sizes = sizes = struct({'zpad': 3000, 'preamble': len(preamble), 'preambleGuard': 40, 'header': 320, 'headerGuard': 100, 'payload': 560, 'payloadGuard': space_between_packets, })
        self.symb_rate = symb_rate = 1250000*2
        self.samp_rate = samp_rate = 5000000
        self.full_header = full_header = sizes.zpad+sizes.preamble+sizes.preambleGuard+ sizes.header + sizes.headerGuard
        self.excess_bw = excess_bw = 0.350
        self.center_freq = center_freq = 433e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	"packet_len",
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(usrp_tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.preamble_vect = blocks.vector_source_c(preamble, True, 1, [])
        self.learning_udp_trigger_0 = learning.udp_trigger(tx_id,'0.0.0.0',port)
        self.learning_head_0 = learning.head(gr.sizeof_gr_complex*1, full_header, True)
        self.digital_psk_mod_1 = digital.psk.psk_mod(
          constellation_points=4,
          mod_code="gray",
          differential=True,
          samples_per_symbol=samp_rate/symb_rate,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=64, cp_len=16,
        	  packet_length_tag_key='length',
        	  bps_header=1,
        	  bps_payload=2,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_b((tx_id, tx_id, tx_id, tx_id, tx_id), False, 1, [])
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b((0,0,0,0,0xA7), True, 1, [])
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.complex_t, 'packet_len')
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', (full_header+sizes.payload + sizes.payloadGuard)/float(full_header))
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, full_header, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 5, "length")
        self.blocks_stream_mux_4 = blocks.stream_mux(gr.sizeof_gr_complex*1, (full_header, sizes.payload, sizes.payloadGuard))
        self.blocks_stream_mux_3 = blocks.stream_mux(gr.sizeof_gr_complex*1, (sizes.zpad, sizes.preamble, sizes.preambleGuard, sizes.header, sizes.headerGuard))
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.complex_t, 'packet_len')
        self.blocks_null_source_2 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(0.05)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blks2_selector_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0 if (is_noise) else 1,
        	output_index=0,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_char*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0 if (is_random_source) else 1,
        	output_index=0,
        )
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_TRI_WAVE, gain_freq, (max_gain-min_gain), min_gain)
        (self.analog_sig_source_x_0_0).set_max_output_buffer(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 256, nb_packets)), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_UNIFORM, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.learning_udp_trigger_0, 'in'))
        self.msg_connect((self.learning_udp_trigger_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blks2_selector_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blks2_selector_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.digital_psk_mod_1, 0))
        self.connect((self.blks2_selector_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_stream_mux_3, 3))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_mux_4, 1))
        self.connect((self.blocks_null_source_1, 0), (self.blocks_stream_mux_4, 2))
        self.connect((self.blocks_null_source_1_0, 0), (self.blocks_stream_mux_3, 2))
        self.connect((self.blocks_null_source_1_0_0, 0), (self.blocks_stream_mux_3, 4))
        self.connect((self.blocks_null_source_2, 0), (self.blocks_stream_mux_3, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_stream_mux_4, 0))
        self.connect((self.blocks_stream_mux_3, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_stream_mux_4, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.learning_head_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blks2_selector_0, 1))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.digital_psk_mod_1, 0), (self.blks2_selector_0_0, 1))
        self.connect((self.learning_head_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.preamble_vect, 0), (self.blocks_stream_mux_3, 1))

    def get_gain_freq(self):
        return self.gain_freq

    def set_gain_freq(self, gain_freq):
        self.gain_freq = gain_freq
        self.analog_sig_source_x_0_0.set_frequency(self.gain_freq)

    def get_is_random_source(self):
        return self.is_random_source

    def set_is_random_source(self, is_random_source):
        self.is_random_source = is_random_source
        self.blks2_selector_0.set_input_index(int(0 if (self.is_random_source) else 1))

    def get_max_gain(self):
        return self.max_gain

    def set_max_gain(self, max_gain):
        self.max_gain = max_gain
        self.analog_sig_source_x_0_0.set_amplitude((self.max_gain-self.min_gain))

    def get_min_gain(self):
        return self.min_gain

    def set_min_gain(self, min_gain):
        self.min_gain = min_gain
        self.analog_sig_source_x_0_0.set_amplitude((self.max_gain-self.min_gain))
        self.analog_sig_source_x_0_0.set_offset(self.min_gain)

    def get_nb_packets(self):
        return self.nb_packets

    def set_nb_packets(self, nb_packets):
        self.nb_packets = nb_packets

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_space_between_packets(self):
        return self.space_between_packets

    def set_space_between_packets(self, space_between_packets):
        self.space_between_packets = space_between_packets

    def get_tx_id(self):
        return self.tx_id

    def set_tx_id(self, tx_id):
        self.tx_id = tx_id
        self.blocks_vector_source_x_0_0_0.set_data((self.tx_id, self.tx_id, self.tx_id, self.tx_id, self.tx_id), [])

    def get_usrp_tx_gain(self):
        return self.usrp_tx_gain

    def set_usrp_tx_gain(self, usrp_tx_gain):
        self.usrp_tx_gain = usrp_tx_gain
        self.uhd_usrp_sink_0.set_gain(self.usrp_tx_gain, 0)


    def get_zeros_offset(self):
        return self.zeros_offset

    def set_zeros_offset(self, zeros_offset):
        self.zeros_offset = zeros_offset

    def get_is_noise(self):
        return self.is_noise

    def set_is_noise(self, is_noise):
        self.is_noise = is_noise
        self.blks2_selector_0_0.set_input_index(int(0 if (self.is_noise) else 1))

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.preamble_vect.set_data(self.preamble, [])

    def get_sizes(self):
        return self.sizes

    def set_sizes(self, sizes):
        self.sizes = sizes

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)

    def get_full_header(self):
        return self.full_header

    def set_full_header(self, full_header):
        self.full_header = full_header
        self.learning_head_0.set_length(self.full_header)
        self.blocks_tagged_stream_multiply_length_0.set_scalar((self.full_header+sizes.payload + sizes.payloadGuard)/float(self.full_header))
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.full_header)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.full_header)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--gain-freq", dest="gain_freq", type="eng_float", default=eng_notation.num_to_str(2),
        help="Set gain_frequency [default=%default]")
    parser.add_option(
        "-R", "--is-random-source", dest="is_random_source", type="intx", default=0,
        help="Set is_random_source [default=%default]")
    parser.add_option(
        "-M", "--max-gain", dest="max_gain", type="eng_float", default=eng_notation.num_to_str(0.1),
        help="Set maximum_gain [default=%default]")
    parser.add_option(
        "-m", "--min-gain", dest="min_gain", type="eng_float", default=eng_notation.num_to_str(0.001),
        help="Set minimum_gain [default=%default]")
    parser.add_option(
        "-N", "--nb-packets", dest="nb_packets", type="intx", default=70000,
        help="Set nb_packets [default=%default]")
    parser.add_option(
        "-L", "--packet-len", dest="packet_len", type="intx", default=400,
        help="Set packet_len [default=%default]")
    parser.add_option(
        "-P", "--port", dest="port", type="intx", default=3580,
        help="Set port_number [default=%default]")
    parser.add_option(
        "-s", "--space-between-packets", dest="space_between_packets", type="intx", default=200,
        help="Set space_between_packets [default=%default]")
    parser.add_option(
        "-T", "--tx-id", dest="tx_id", type="intx", default=0,
        help="Set tx_id [default=%default]")
    parser.add_option(
        "-G", "--usrp-tx-gain", dest="usrp_tx_gain", type="intx", default=3,
        help="Set gain [default=%default]")
    parser.add_option(
        "-O", "--zeros-offset", dest="zeros_offset", type="intx", default=100004,
        help="Set zeros_offset [default=%default]")
    parser.add_option(
        "-r", "--is-noise", dest="is_noise", type="intx", default=0,
        help="Set is_noise [default=%default]")
    return parser


def main(top_block_cls=emitter, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(gain_freq=options.gain_freq, is_random_source=options.is_random_source, max_gain=options.max_gain, min_gain=options.min_gain, nb_packets=options.nb_packets, packet_len=options.packet_len, port=options.port, space_between_packets=options.space_between_packets, tx_id=options.tx_id, usrp_tx_gain=options.usrp_tx_gain, zeros_offset=options.zeros_offset, is_noise=options.is_noise)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
