#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx Id Reciever
# Author: Cyrille Morin
# GNU Radio version: 3.10.5.1

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
from gnuradio import txid
from gnuradio import uhd
import time




class reciever(gr.top_block):

    def __init__(self, center_freq=433e6, file='enreg', nb_payloads_to_save=((50000 + 2000)), samp_rate=5000000, tx_amount=21, usrp_rx_gain=25):
        gr.top_block.__init__(self, "Tx Id Reciever", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.file = file
        self.nb_payloads_to_save = nb_payloads_to_save
        self.samp_rate = samp_rate
        self.tx_amount = tx_amount
        self.usrp_rx_gain = usrp_rx_gain

        ##################################################
        # Variables
        ##################################################
        self.preamble = preamble = (1.00000000000000 + 0.00000000000000j, -0.0198821876650702 - 0.999802329770066j, 0.0596151251698190 + 0.998221436781933j, -0.992892073701974 + 0.119018191801903j, -0.980297366804636 + 0.197527397177953j, 0.293850274337919 + 0.955851461405761j, -0.405525320812986 - 0.914083811354038j, 0.848983362091364 - 0.528419578452620j, 0.754564620158230 - 0.656225749270376j, -0.780057308185211 - 0.625708075660561j, 0.888282612749130 + 0.459297289222982j, -0.255616632440464 + 0.966778225458040j, -0.0198821876650804 + 0.999802329770065j, 0.971669340040416 - 0.236344438532879j, -0.869320274439587 + 0.494249188616716j, -0.727878810369485 - 0.685705795086423j, -0.905840393665518 - 0.423619146408540j, -0.0992537989080696 + 0.995062150522427j, -0.255616632440477 - 0.966778225458036j, 0.804316565270771 - 0.594201028971703j, 0.511435479103437 - 0.859321680579653j, -0.992892073701971 - 0.119018191801923j, 0.949820131727787 - 0.312796607022213j, 0.700042074569421 + 0.714101599096754j, 0.949820131727768 + 0.312796607022273j, -0.177997895677522 - 0.984030867978426j, 0.641093637592130 + 0.767462668693983j, -0.331619278552096 + 0.943413299722125j, 0.216978808106213 + 0.976176314419074j, 0.700042074569433 - 0.714101599096743j, -0.177997895677626 + 0.984030867978407j, -0.905840393665558 + 0.423619146408453j, -0.476867501428628 + 0.878975190822367j, 0.987375341936355 - 0.158398024407083j, -0.671098428359002 + 0.741368261698650j, -0.999209397227295 - 0.0397565150970890j, -0.780057308185194 + 0.625708075660582j, 0.987375341936324 + 0.158398024407273j, -0.827304032543040 + 0.561754428320796j, -0.980297366804605 - 0.197527397178109j, -0.827304032543027 + 0.561754428320816j, 0.987375341936332 + 0.158398024407226j, -0.780057308185292 + 0.625708075660460j, -0.999209397227299 - 0.0397565150969950j, -0.671098428359083 + 0.741368261698577j, 0.987375341936350 - 0.158398024407110j, -0.476867501428484 + 0.878975190822446j, -0.905840393665478 + 0.423619146408624j, -0.177997895677642 + 0.984030867978404j, 0.700042074569508 - 0.714101599096669j, 0.216978808106132 + 0.976176314419092j, -0.331619278552151 + 0.943413299722105j, 0.641093637592190 + 0.767462668693933j, -0.177997895677511 - 0.984030867978428j, 0.949820131727754 + 0.312796607022316j, 0.700042074569284 + 0.714101599096888j, 0.949820131727893 - 0.312796607021891j, -0.992892073701961 - 0.119018191802010j, 0.511435479103736 - 0.859321680579474j, 0.804316565270626 - 0.594201028971898j, -0.255616632440350 - 0.966778225458070j, -0.0992537989081486 + 0.995062150522419j, -0.905840393665482 - 0.423619146408617j, -0.727878810369385 - 0.685705795086529j, -0.869320274439717 + 0.494249188616486j, 0.971669340040621 - 0.236344438532038j, -0.0198821876652695 + 0.999802329770062j, -0.255616632440926 + 0.966778225457918j, 0.888282612749188 + 0.459297289222869j, -0.780057308185057 - 0.625708075660753j, 0.754564620158670 - 0.656225749269870j, 0.848983362091728 - 0.528419578452034j, -0.405525320812299 - 0.914083811354343j, 0.293850274337947 + 0.955851461405753j, -0.980297366804665 + 0.197527397177809j, -0.992892073702018 + 0.119018191801536j, 0.0596151251691726 + 0.998221436781972j, -0.0198821876650031 - 0.999802329770067j, 1.00000000000000 + 4.46840285540623e-13j)

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('internal', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_gain(usrp_rx_gain, 0)
        self.txid_record_payload_0 = txid.record_payload((tx_amount+5), file, (len(preamble) + 300), 600, False, '127.0.0.1', 3581, nb_payloads_to_save)
        self.txid_packet_isolator_c_0 = txid.packet_isolator_c(979, 100, 200, "corr_est")
        self.txid_packet_isolator_c_0.set_min_output_buffer(2000)
        self.txid_correlator_0 = txid.correlator(preamble, 1, 0, 0.3, digital.THRESHOLD_ABSOLUTE)
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
            fft_len=64, cp_len=16,
            frame_length_tag_key='frame_'+"rx_len",
            packet_length_tag_key="rx_len",
            bps_header=1,
            bps_payload=2,
            debug_log=False,
            scramble_bits=False)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 1000000)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_skiphead_0, 0), (self.txid_correlator_0, 0))
        self.connect((self.digital_ofdm_rx_0, 0), (self.txid_record_payload_0, 0))
        self.connect((self.txid_correlator_0, 0), (self.txid_packet_isolator_c_0, 0))
        self.connect((self.txid_packet_isolator_c_0, 0), (self.digital_ofdm_rx_0, 0))
        self.connect((self.txid_packet_isolator_c_0, 0), (self.txid_record_payload_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_skiphead_0, 0))


    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file

    def get_nb_payloads_to_save(self):
        return self.nb_payloads_to_save

    def set_nb_payloads_to_save(self, nb_payloads_to_save):
        self.nb_payloads_to_save = nb_payloads_to_save

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_tx_amount(self):
        return self.tx_amount

    def set_tx_amount(self, tx_amount):
        self.tx_amount = tx_amount

    def get_usrp_rx_gain(self):
        return self.usrp_rx_gain

    def set_usrp_rx_gain(self, usrp_rx_gain):
        self.usrp_rx_gain = usrp_rx_gain
        self.uhd_usrp_source_0.set_gain(self.usrp_rx_gain, 0)

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--center-freq", dest="center_freq", type=eng_float, default=eng_notation.num_to_str(float(433e6)),
        help="Set Center frequency [default=%(default)r]")
    parser.add_argument(
        "-F", "--file", dest="file", type=str, default='enreg',
        help="Set Base Filename [default=%(default)r]")
    parser.add_argument(
        "-r", "--nb-payloads-to-save", dest="nb_payloads_to_save", type=intx, default=((50000 + 2000)),
        help="Set Payloads to save [default=%(default)r]")
    parser.add_argument(
        "-a", "--samp-rate", dest="samp_rate", type=intx, default=5000000,
        help="Set Sample rate [default=%(default)r]")
    parser.add_argument(
        "-T", "--tx-amount", dest="tx_amount", type=intx, default=21,
        help="Set Transmitter amount [default=%(default)r]")
    parser.add_argument(
        "-g", "--usrp-rx-gain", dest="usrp_rx_gain", type=eng_float, default=eng_notation.num_to_str(float(25)),
        help="Set RX Gain [default=%(default)r]")
    return parser


def main(top_block_cls=reciever, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(center_freq=options.center_freq, file=options.file, nb_payloads_to_save=options.nb_payloads_to_save, samp_rate=options.samp_rate, tx_amount=options.tx_amount, usrp_rx_gain=options.usrp_rx_gain)

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
