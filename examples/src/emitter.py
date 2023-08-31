#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx Id Emitter
# Author: Cyrille Morin
# GNU Radio version: 3.10.6.0

def struct(data): return type('Struct', (object,), data)()
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import txid
from gnuradio import uhd
import time




class emitter(gr.top_block):

    def __init__(self, center_freq=433e6, filter_width=0, gain_freq=2, is_noise=0, is_random_source=0, max_gain=0.1, min_gain=0.001, nb_packets=70000, packet_len=400, port=3580, samp_rate=5000000, space_between_packets=200, tx_id=0, usrp_tx_gain=3):
        gr.top_block.__init__(self, "Tx Id Emitter", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.filter_width = filter_width
        self.gain_freq = gain_freq
        self.is_noise = is_noise
        self.is_random_source = is_random_source
        self.max_gain = max_gain
        self.min_gain = min_gain
        self.nb_packets = nb_packets
        self.packet_len = packet_len
        self.port = port
        self.samp_rate = samp_rate
        self.space_between_packets = space_between_packets
        self.tx_id = tx_id
        self.usrp_tx_gain = usrp_tx_gain

        ##################################################
        # Variables
        ##################################################
        self.preamble = preamble = (1.00000000000000 + 0.00000000000000j, -0.0198821876650702 - 0.999802329770066j, 0.0596151251698190 + 0.998221436781933j, -0.992892073701974 + 0.119018191801903j, -0.980297366804636 + 0.197527397177953j, 0.293850274337919 + 0.955851461405761j, -0.405525320812986 - 0.914083811354038j, 0.848983362091364 - 0.528419578452620j, 0.754564620158230 - 0.656225749270376j, -0.780057308185211 - 0.625708075660561j, 0.888282612749130 + 0.459297289222982j, -0.255616632440464 + 0.966778225458040j, -0.0198821876650804 + 0.999802329770065j, 0.971669340040416 - 0.236344438532879j, -0.869320274439587 + 0.494249188616716j, -0.727878810369485 - 0.685705795086423j, -0.905840393665518 - 0.423619146408540j, -0.0992537989080696 + 0.995062150522427j, -0.255616632440477 - 0.966778225458036j, 0.804316565270771 - 0.594201028971703j, 0.511435479103437 - 0.859321680579653j, -0.992892073701971 - 0.119018191801923j, 0.949820131727787 - 0.312796607022213j, 0.700042074569421 + 0.714101599096754j, 0.949820131727768 + 0.312796607022273j, -0.177997895677522 - 0.984030867978426j, 0.641093637592130 + 0.767462668693983j, -0.331619278552096 + 0.943413299722125j, 0.216978808106213 + 0.976176314419074j, 0.700042074569433 - 0.714101599096743j, -0.177997895677626 + 0.984030867978407j, -0.905840393665558 + 0.423619146408453j, -0.476867501428628 + 0.878975190822367j, 0.987375341936355 - 0.158398024407083j, -0.671098428359002 + 0.741368261698650j, -0.999209397227295 - 0.0397565150970890j, -0.780057308185194 + 0.625708075660582j, 0.987375341936324 + 0.158398024407273j, -0.827304032543040 + 0.561754428320796j, -0.980297366804605 - 0.197527397178109j, -0.827304032543027 + 0.561754428320816j, 0.987375341936332 + 0.158398024407226j, -0.780057308185292 + 0.625708075660460j, -0.999209397227299 - 0.0397565150969950j, -0.671098428359083 + 0.741368261698577j, 0.987375341936350 - 0.158398024407110j, -0.476867501428484 + 0.878975190822446j, -0.905840393665478 + 0.423619146408624j, -0.177997895677642 + 0.984030867978404j, 0.700042074569508 - 0.714101599096669j, 0.216978808106132 + 0.976176314419092j, -0.331619278552151 + 0.943413299722105j, 0.641093637592190 + 0.767462668693933j, -0.177997895677511 - 0.984030867978428j, 0.949820131727754 + 0.312796607022316j, 0.700042074569284 + 0.714101599096888j, 0.949820131727893 - 0.312796607021891j, -0.992892073701961 - 0.119018191802010j, 0.511435479103736 - 0.859321680579474j, 0.804316565270626 - 0.594201028971898j, -0.255616632440350 - 0.966778225458070j, -0.0992537989081486 + 0.995062150522419j, -0.905840393665482 - 0.423619146408617j, -0.727878810369385 - 0.685705795086529j, -0.869320274439717 + 0.494249188616486j, 0.971669340040621 - 0.236344438532038j, -0.0198821876652695 + 0.999802329770062j, -0.255616632440926 + 0.966778225457918j, 0.888282612749188 + 0.459297289222869j, -0.780057308185057 - 0.625708075660753j, 0.754564620158670 - 0.656225749269870j, 0.848983362091728 - 0.528419578452034j, -0.405525320812299 - 0.914083811354343j, 0.293850274337947 + 0.955851461405753j, -0.980297366804665 + 0.197527397177809j, -0.992892073702018 + 0.119018191801536j, 0.0596151251691726 + 0.998221436781972j, -0.0198821876650031 - 0.999802329770067j, 1.00000000000000 + 4.46840285540623e-13j)
        self.zpad = zpad = 3000
        self.preamble_len = preamble_len = len(preamble)
        self.preamble_guard_len = preamble_guard_len = 40
        self.header_len = header_len = 320
        self.header_guard_len = header_guard_len = 100
        self.sizes = sizes = struct({

            'zpad': 3000,

            'preamble': len(preamble),

            'preambleGuard': 40,

            'header': 320,

            'headerGuard': 100,

            'payload': 560,

            'payloadGuard': space_between_packets,













        })
        self.qpsk = qpsk = digital.constellation_qpsk().base()
        self.payload_len = payload_len = 560
        self.payload_guard_len = payload_guard_len = 200
        self.full_header = full_header = zpad+preamble_len+preamble_guard_len+ header_len + header_guard_len
        self.excess_bw = excess_bw = 0.350

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "packet_len",
        )
        self.uhd_usrp_sink_0.set_clock_source('internal', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_gain(usrp_tx_gain, 0)
        self.txid_udp_trigger_0 = txid.udp_trigger(tx_id, '0.0.0.0', port)
        self.txid_head_0 = txid.head(gr.sizeof_gr_complex*1, full_header, True)
        self.preamble_vect = blocks.vector_source_c(preamble, True, 1, [])
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.complex_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.complex_t, 'packet_len')
        self.null_3 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.null_2 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.null_1 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.null_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
            fft_len=64,
            cp_len=16,
            packet_length_tag_key='length',
            bps_header=1,
            bps_payload=2,
            rolloff=0,
            debug_log=False,
            scramble_bits=False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=2,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_b((tx_id, tx_id, tx_id, tx_id, tx_id), False, 1, [])
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b((0,0,0,0,0xA7), True, 1, [])
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', ((full_header+payload_len + payload_guard_len)/float(full_header)))
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, full_header, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 5, "length")
        self.blocks_stream_mux_4 = blocks.stream_mux(gr.sizeof_gr_complex*1, [full_header, payload_len, payload_guard_len])
        self.blocks_stream_mux_3 = blocks.stream_mux(gr.sizeof_gr_complex*1, [zpad, preamble_len, preamble_guard_len, header_len, header_guard_len])
        self.blocks_selector_1 = blocks.selector(gr.sizeof_char*1,0 if (is_random_source) else 1,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0 if (is_noise) else 1,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, payload_len)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(0.05, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(100, analog.GR_TRI_WAVE, gain_freq, ((max_gain-min_gain)), min_gain, 0)
        self.analog_sig_source_x_0_0.set_max_output_buffer(1)
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 256, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_UNIFORM, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.txid_udp_trigger_0, 'in'))
        self.msg_connect((self.txid_udp_trigger_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_stream_mux_3, 3))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_mux_4, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_stream_mux_3, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_stream_mux_4, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.txid_head_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.null_0, 0), (self.blocks_stream_mux_3, 0))
        self.connect((self.null_1, 0), (self.blocks_stream_mux_3, 2))
        self.connect((self.null_2, 0), (self.blocks_stream_mux_3, 4))
        self.connect((self.null_3, 0), (self.blocks_stream_mux_4, 2))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_stream_mux_4, 0))
        self.connect((self.preamble_vect, 0), (self.blocks_stream_mux_3, 1))
        self.connect((self.txid_head_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))


    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)

    def get_filter_width(self):
        return self.filter_width

    def set_filter_width(self, filter_width):
        self.filter_width = filter_width
        self.uhd_usrp_sink_0.set_bandwidth(self.filter_width, 0)

    def get_gain_freq(self):
        return self.gain_freq

    def set_gain_freq(self, gain_freq):
        self.gain_freq = gain_freq
        self.analog_sig_source_x_0_0.set_frequency(self.gain_freq)

    def get_is_noise(self):
        return self.is_noise

    def set_is_noise(self, is_noise):
        self.is_noise = is_noise
        self.blocks_selector_0.set_input_index(0 if (self.is_noise) else 1)

    def get_is_random_source(self):
        return self.is_random_source

    def set_is_random_source(self, is_random_source):
        self.is_random_source = is_random_source
        self.blocks_selector_1.set_input_index(0 if (self.is_random_source) else 1)

    def get_max_gain(self):
        return self.max_gain

    def set_max_gain(self, max_gain):
        self.max_gain = max_gain
        self.analog_sig_source_x_0_0.set_amplitude(((self.max_gain-self.min_gain)))

    def get_min_gain(self):
        return self.min_gain

    def set_min_gain(self, min_gain):
        self.min_gain = min_gain
        self.analog_sig_source_x_0_0.set_amplitude(((self.max_gain-self.min_gain)))
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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

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

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.set_preamble_len(len(self.preamble))
        self.preamble_vect.set_data(self.preamble, [])

    def get_zpad(self):
        return self.zpad

    def set_zpad(self, zpad):
        self.zpad = zpad
        self.set_full_header(self.zpad+self.preamble_len+self.preamble_guard_len+ self.header_len + self.header_guard_len)

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_full_header(self.zpad+self.preamble_len+self.preamble_guard_len+ self.header_len + self.header_guard_len)

    def get_preamble_guard_len(self):
        return self.preamble_guard_len

    def set_preamble_guard_len(self, preamble_guard_len):
        self.preamble_guard_len = preamble_guard_len
        self.set_full_header(self.zpad+self.preamble_len+self.preamble_guard_len+ self.header_len + self.header_guard_len)

    def get_header_len(self):
        return self.header_len

    def set_header_len(self, header_len):
        self.header_len = header_len
        self.set_full_header(self.zpad+self.preamble_len+self.preamble_guard_len+ self.header_len + self.header_guard_len)

    def get_header_guard_len(self):
        return self.header_guard_len

    def set_header_guard_len(self, header_guard_len):
        self.header_guard_len = header_guard_len
        self.set_full_header(self.zpad+self.preamble_len+self.preamble_guard_len+ self.header_len + self.header_guard_len)

    def get_sizes(self):
        return self.sizes

    def set_sizes(self, sizes):
        self.sizes = sizes

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.blocks_repeat_0.set_interpolation(self.payload_len)
        self.blocks_tagged_stream_multiply_length_0.set_scalar(((self.full_header+self.payload_len + self.payload_guard_len)/float(self.full_header)))

    def get_payload_guard_len(self):
        return self.payload_guard_len

    def set_payload_guard_len(self, payload_guard_len):
        self.payload_guard_len = payload_guard_len
        self.blocks_tagged_stream_multiply_length_0.set_scalar(((self.full_header+self.payload_len + self.payload_guard_len)/float(self.full_header)))

    def get_full_header(self):
        return self.full_header

    def set_full_header(self, full_header):
        self.full_header = full_header
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.full_header)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.full_header)
        self.blocks_tagged_stream_multiply_length_0.set_scalar(((self.full_header+self.payload_len + self.payload_guard_len)/float(self.full_header)))
        self.txid_head_0.set_length(self.full_header)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--center-freq", dest="center_freq", type=eng_float, default=eng_notation.num_to_str(float(433e6)),
        help="Set Center frequency [default=%(default)r]")
    parser.add_argument(
        "-b", "--filter-width", dest="filter_width", type=eng_float, default=eng_notation.num_to_str(float(0)),
        help="Set Tx Filter Bandwidth [default=%(default)r]")
    parser.add_argument(
        "-f", "--gain-freq", dest="gain_freq", type=eng_float, default=eng_notation.num_to_str(float(2)),
        help="Set gain_frequency [default=%(default)r]")
    parser.add_argument(
        "-r", "--is-noise", dest="is_noise", type=intx, default=0,
        help="Set is_noise [default=%(default)r]")
    parser.add_argument(
        "-R", "--is-random-source", dest="is_random_source", type=intx, default=0,
        help="Set is_random_source [default=%(default)r]")
    parser.add_argument(
        "-M", "--max-gain", dest="max_gain", type=eng_float, default=eng_notation.num_to_str(float(0.1)),
        help="Set maximum_gain [default=%(default)r]")
    parser.add_argument(
        "-m", "--min-gain", dest="min_gain", type=eng_float, default=eng_notation.num_to_str(float(0.001)),
        help="Set minimum_gain [default=%(default)r]")
    parser.add_argument(
        "-N", "--nb-packets", dest="nb_packets", type=intx, default=70000,
        help="Set nb_packets [default=%(default)r]")
    parser.add_argument(
        "-L", "--packet-len", dest="packet_len", type=intx, default=400,
        help="Set packet_len [default=%(default)r]")
    parser.add_argument(
        "-P", "--port", dest="port", type=intx, default=3580,
        help="Set port_number [default=%(default)r]")
    parser.add_argument(
        "-a", "--samp-rate", dest="samp_rate", type=intx, default=5000000,
        help="Set Sample rate [default=%(default)r]")
    parser.add_argument(
        "-s", "--space-between-packets", dest="space_between_packets", type=intx, default=200,
        help="Set space_between_packets [default=%(default)r]")
    parser.add_argument(
        "-T", "--tx-id", dest="tx_id", type=intx, default=0,
        help="Set tx_id [default=%(default)r]")
    parser.add_argument(
        "-G", "--usrp-tx-gain", dest="usrp_tx_gain", type=intx, default=3,
        help="Set gain [default=%(default)r]")
    return parser


def main(top_block_cls=emitter, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(center_freq=options.center_freq, filter_width=options.filter_width, gain_freq=options.gain_freq, is_noise=options.is_noise, is_random_source=options.is_random_source, max_gain=options.max_gain, min_gain=options.min_gain, nb_packets=options.nb_packets, packet_len=options.packet_len, port=options.port, samp_rate=options.samp_rate, space_between_packets=options.space_between_packets, tx_id=options.tx_id, usrp_tx_gain=options.usrp_tx_gain)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
