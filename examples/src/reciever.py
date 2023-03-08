#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Reciever
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import iio
from gnuradio import txid



from gnuradio import qtgui

class reciever(gr.top_block, Qt.QWidget):

    def __init__(self, file_im='enreg_im', file_re='enreg_re', gain_freq=2, is_noise=0, is_random_source=0, max_gain=0.1, min_gain=0.001, nb_packets=70000, nb_samples_to_save=(600*(50000 + 2000)), packet_len=400, port=3580, space_between_packets=200, tx_amount=21, tx_id=0, usrp_tx_gain=3):
        gr.top_block.__init__(self, "Reciever", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Reciever")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "reciever")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.file_im = file_im
        self.file_re = file_re
        self.gain_freq = gain_freq
        self.is_noise = is_noise
        self.is_random_source = is_random_source
        self.max_gain = max_gain
        self.min_gain = min_gain
        self.nb_packets = nb_packets
        self.nb_samples_to_save = nb_samples_to_save
        self.packet_len = packet_len
        self.port = port
        self.space_between_packets = space_between_packets
        self.tx_amount = tx_amount
        self.tx_id = tx_id
        self.usrp_tx_gain = usrp_tx_gain

        ##################################################
        # Variables
        ##################################################
        self.zpad = zpad = 3000
        self.preamble_len = preamble_len = 80
        self.preamble_guard_len = preamble_guard_len = 40
        self.header_len = header_len = 320
        self.header_guard_len = header_guard_len = 100
        self.usrp_rx_gain = usrp_rx_gain = 30
        self.samp_rate = samp_rate = 5000000
        self.qpsk = qpsk = digital.constellation_qpsk().base()
        self.preamble = preamble = (1.00000000000000 + 0.00000000000000j, -0.0198821876650702 - 0.999802329770066j, 0.0596151251698190 + 0.998221436781933j, -0.992892073701974 + 0.119018191801903j, -0.980297366804636 + 0.197527397177953j, 0.293850274337919 + 0.955851461405761j, -0.405525320812986 - 0.914083811354038j, 0.848983362091364 - 0.528419578452620j, 0.754564620158230 - 0.656225749270376j, -0.780057308185211 - 0.625708075660561j, 0.888282612749130 + 0.459297289222982j, -0.255616632440464 + 0.966778225458040j, -0.0198821876650804 + 0.999802329770065j, 0.971669340040416 - 0.236344438532879j, -0.869320274439587 + 0.494249188616716j, -0.727878810369485 - 0.685705795086423j, -0.905840393665518 - 0.423619146408540j, -0.0992537989080696 + 0.995062150522427j, -0.255616632440477 - 0.966778225458036j, 0.804316565270771 - 0.594201028971703j, 0.511435479103437 - 0.859321680579653j, -0.992892073701971 - 0.119018191801923j, 0.949820131727787 - 0.312796607022213j, 0.700042074569421 + 0.714101599096754j, 0.949820131727768 + 0.312796607022273j, -0.177997895677522 - 0.984030867978426j, 0.641093637592130 + 0.767462668693983j, -0.331619278552096 + 0.943413299722125j, 0.216978808106213 + 0.976176314419074j, 0.700042074569433 - 0.714101599096743j, -0.177997895677626 + 0.984030867978407j, -0.905840393665558 + 0.423619146408453j, -0.476867501428628 + 0.878975190822367j, 0.987375341936355 - 0.158398024407083j, -0.671098428359002 + 0.741368261698650j, -0.999209397227295 - 0.0397565150970890j, -0.780057308185194 + 0.625708075660582j, 0.987375341936324 + 0.158398024407273j, -0.827304032543040 + 0.561754428320796j, -0.980297366804605 - 0.197527397178109j, -0.827304032543027 + 0.561754428320816j, 0.987375341936332 + 0.158398024407226j, -0.780057308185292 + 0.625708075660460j, -0.999209397227299 - 0.0397565150969950j, -0.671098428359083 + 0.741368261698577j, 0.987375341936350 - 0.158398024407110j, -0.476867501428484 + 0.878975190822446j, -0.905840393665478 + 0.423619146408624j, -0.177997895677642 + 0.984030867978404j, 0.700042074569508 - 0.714101599096669j, 0.216978808106132 + 0.976176314419092j, -0.331619278552151 + 0.943413299722105j, 0.641093637592190 + 0.767462668693933j, -0.177997895677511 - 0.984030867978428j, 0.949820131727754 + 0.312796607022316j, 0.700042074569284 + 0.714101599096888j, 0.949820131727893 - 0.312796607021891j, -0.992892073701961 - 0.119018191802010j, 0.511435479103736 - 0.859321680579474j, 0.804316565270626 - 0.594201028971898j, -0.255616632440350 - 0.966778225458070j, -0.0992537989081486 + 0.995062150522419j, -0.905840393665482 - 0.423619146408617j, -0.727878810369385 - 0.685705795086529j, -0.869320274439717 + 0.494249188616486j, 0.971669340040621 - 0.236344438532038j, -0.0198821876652695 + 0.999802329770062j, -0.255616632440926 + 0.966778225457918j, 0.888282612749188 + 0.459297289222869j, -0.780057308185057 - 0.625708075660753j, 0.754564620158670 - 0.656225749269870j, 0.848983362091728 - 0.528419578452034j, -0.405525320812299 - 0.914083811354343j, 0.293850274337947 + 0.955851461405753j, -0.980297366804665 + 0.197527397177809j, -0.992892073702018 + 0.119018191801536j, 0.0596151251691726 + 0.998221436781972j, -0.0198821876650031 - 0.999802329770067j, 1.00000000000000 + 4.46840285540623e-13j)
        self.payload_len = payload_len = 560
        self.payload_guard_len = payload_guard_len = 200
        self.full_header = full_header = zpad+preamble_len+preamble_guard_len+ header_len + header_guard_len
        self.excess_bw = excess_bw = 0.350
        self.center_freq = center_freq = 433e6

        ##################################################
        # Blocks
        ##################################################

        self.txid_udp_trigger_0 = txid.udp_trigger(tx_id, '127.0.0.1', port)
        self.txid_packet_isolator_c_0 = txid.packet_isolator_c(980, 100, 200, "corr_est")
        self.txid_packet_isolator_c_0.set_min_output_buffer(2000)
        self.txid_head_0_2 = txid.head(gr.sizeof_gr_complex*1, full_header, True)
        self.txid_head_0_1 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_9 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_8 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_7_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_7 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_6_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_6 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_5_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_5 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_4_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_4 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_3_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_3 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_2_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_2 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_1_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_1 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_0_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_head_0 = txid.head(gr.sizeof_gr_complex*1, nb_samples_to_save, False)
        self.txid_data_switch_0 = txid.data_switch(tx_amount, 380, 600, False, '127.0.0.1', 3581)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.preamble_vect = blocks.vector_source_c(preamble, True, 1, [])
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.complex_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.complex_t, 'packet_len')
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('ip:pluto2.local' if 'ip:pluto2.local' else iio.get_pluto_uri(), [True, True], 100000)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(int(center_freq))
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('ip:pluto2.local' if 'ip:pluto2.local' else iio.get_pluto_uri(), [True, True], 4096, False)
        self.iio_pluto_sink_0.set_len_tag_key('packet_len')
        self.iio_pluto_sink_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0.set_frequency(int(center_freq))
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, 80-usrp_tx_gain)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
            fft_len=64,
            cp_len=16,
            packet_length_tag_key='length',
            occupied_carriers=(),
            pilot_carriers=(),
            pilot_symbols=(),
            sync_word1=(),
            sync_word2=(),
            bps_header=1,
            bps_payload=2,
            rolloff=0,
            debug_log=False,
            scramble_bits=False)
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
            fft_len=64, cp_len=16,
            frame_length_tag_key='frame_'+"rx_len",
            packet_length_tag_key="rx_len",
            occupied_carriers=(),
            pilot_carriers=(),
            pilot_symbols=(),
            sync_word1=(),
            sync_word2=(),
            bps_header=1,
            bps_payload=2,
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
        self.blocks_stream_mux_4 = blocks.stream_mux(gr.sizeof_gr_complex*1, full_header, payload_len, payload_guard_len)
        self.blocks_stream_mux_3 = blocks.stream_mux(gr.sizeof_gr_complex*1, zpad, preamble_len, preamble_guard_len, header_len, header_guard_len)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 1000000)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_char*1,0 if (is_random_source) else 1,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0 if (is_noise) else 1,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_source_2 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(0.05, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0_3 = blocks.file_sink(gr.sizeof_float*1, file_re+'_11'+'.bin', False)
        self.blocks_file_sink_0_3.set_unbuffered(False)
        self.blocks_file_sink_0_1_9 = blocks.file_sink(gr.sizeof_float*1, file_re+'_12'+'.bin', False)
        self.blocks_file_sink_0_1_9.set_unbuffered(False)
        self.blocks_file_sink_0_1_8 = blocks.file_sink(gr.sizeof_float*1, file_re+'_10'+'.bin', False)
        self.blocks_file_sink_0_1_8.set_unbuffered(False)
        self.blocks_file_sink_0_1_7_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_20'+'.bin', False)
        self.blocks_file_sink_0_1_7_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_7 = blocks.file_sink(gr.sizeof_float*1, file_re+'_9'+'.bin', False)
        self.blocks_file_sink_0_1_7.set_unbuffered(False)
        self.blocks_file_sink_0_1_6_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_19'+'.bin', False)
        self.blocks_file_sink_0_1_6_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_6 = blocks.file_sink(gr.sizeof_float*1, file_re+'_8'+'.bin', False)
        self.blocks_file_sink_0_1_6.set_unbuffered(False)
        self.blocks_file_sink_0_1_5_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_18'+'.bin', False)
        self.blocks_file_sink_0_1_5_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_5 = blocks.file_sink(gr.sizeof_float*1, file_re+'_7'+'.bin', False)
        self.blocks_file_sink_0_1_5.set_unbuffered(False)
        self.blocks_file_sink_0_1_4_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_17'+'.bin', False)
        self.blocks_file_sink_0_1_4_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_4 = blocks.file_sink(gr.sizeof_float*1, file_re+'_6'+'.bin', False)
        self.blocks_file_sink_0_1_4.set_unbuffered(False)
        self.blocks_file_sink_0_1_3_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_16'+'.bin', False)
        self.blocks_file_sink_0_1_3_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_3 = blocks.file_sink(gr.sizeof_float*1, file_re+'_5'+'.bin', False)
        self.blocks_file_sink_0_1_3.set_unbuffered(False)
        self.blocks_file_sink_0_1_2_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_15'+'.bin', False)
        self.blocks_file_sink_0_1_2_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_2 = blocks.file_sink(gr.sizeof_float*1, file_re+'_4'+'.bin', False)
        self.blocks_file_sink_0_1_2.set_unbuffered(False)
        self.blocks_file_sink_0_1_1_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_14'+'.bin', False)
        self.blocks_file_sink_0_1_1_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_1 = blocks.file_sink(gr.sizeof_float*1, file_re+'_3'+'.bin', False)
        self.blocks_file_sink_0_1_1.set_unbuffered(False)
        self.blocks_file_sink_0_1_0_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_13'+'.bin', False)
        self.blocks_file_sink_0_1_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_2'+'.bin', False)
        self.blocks_file_sink_0_1_0.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_float*1, file_re+'_1'+'.bin', False)
        self.blocks_file_sink_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0_2 = blocks.file_sink(gr.sizeof_float*1, file_im+'_11'+'.bin', False)
        self.blocks_file_sink_0_0_2.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_9 = blocks.file_sink(gr.sizeof_float*1, file_im+'_12'+'.bin', False)
        self.blocks_file_sink_0_0_0_9.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_8 = blocks.file_sink(gr.sizeof_float*1, file_im+'_10'+'.bin', False)
        self.blocks_file_sink_0_0_0_8.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_7_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_20'+'.bin', False)
        self.blocks_file_sink_0_0_0_7_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_7 = blocks.file_sink(gr.sizeof_float*1, file_im+'_9'+'.bin', False)
        self.blocks_file_sink_0_0_0_7.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_6_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_19'+'.bin', False)
        self.blocks_file_sink_0_0_0_6_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_6 = blocks.file_sink(gr.sizeof_float*1, file_im+'_8'+'.bin', False)
        self.blocks_file_sink_0_0_0_6.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_5_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_18'+'.bin', False)
        self.blocks_file_sink_0_0_0_5_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_5 = blocks.file_sink(gr.sizeof_float*1, file_im+'_7'+'.bin', False)
        self.blocks_file_sink_0_0_0_5.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_4_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_17'+'.bin', False)
        self.blocks_file_sink_0_0_0_4_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_4 = blocks.file_sink(gr.sizeof_float*1, file_im+'_6'+'.bin', False)
        self.blocks_file_sink_0_0_0_4.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_3_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_16'+'.bin', False)
        self.blocks_file_sink_0_0_0_3_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_3 = blocks.file_sink(gr.sizeof_float*1, file_im+'_5'+'.bin', False)
        self.blocks_file_sink_0_0_0_3.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_2_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_15'+'.bin', False)
        self.blocks_file_sink_0_0_0_2_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_2 = blocks.file_sink(gr.sizeof_float*1, file_im+'_4'+'.bin', False)
        self.blocks_file_sink_0_0_0_2.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_1_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_14'+'.bin', False)
        self.blocks_file_sink_0_0_0_1_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_1 = blocks.file_sink(gr.sizeof_float*1, file_im+'_3'+'.bin', False)
        self.blocks_file_sink_0_0_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_13'+'.bin', False)
        self.blocks_file_sink_0_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_2'+'.bin', False)
        self.blocks_file_sink_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_1'+'.bin', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*1, file_im+'_0'+'.bin', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file_re+'_0'+'.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_float_1_2 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_9 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_8 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_7_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_7 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_6_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_6 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_5_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_5 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_4_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_4 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_3_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_3 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_2_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_2 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_1_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_TRI_WAVE, gain_freq, ((max_gain-min_gain)), min_gain, 0)
        self.analog_sig_source_x_0_0.set_max_output_buffer(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, nb_packets))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_UNIFORM, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.txid_udp_trigger_0, 'in'))
        self.msg_connect((self.txid_udp_trigger_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_complex_to_float_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_complex_to_float_1, 1), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_complex_to_float_1_0, 1), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_1_0, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.blocks_complex_to_float_1_0_0, 1), (self.blocks_file_sink_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_0, 0), (self.blocks_file_sink_0_1_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_0_0, 0), (self.blocks_file_sink_0_1_0_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_1, 1), (self.blocks_file_sink_0_0_0_1, 0))
        self.connect((self.blocks_complex_to_float_1_0_1, 0), (self.blocks_file_sink_0_1_1, 0))
        self.connect((self.blocks_complex_to_float_1_0_1_0, 1), (self.blocks_file_sink_0_0_0_1_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_1_0, 0), (self.blocks_file_sink_0_1_1_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_2, 1), (self.blocks_file_sink_0_0_0_2, 0))
        self.connect((self.blocks_complex_to_float_1_0_2, 0), (self.blocks_file_sink_0_1_2, 0))
        self.connect((self.blocks_complex_to_float_1_0_2_0, 1), (self.blocks_file_sink_0_0_0_2_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_2_0, 0), (self.blocks_file_sink_0_1_2_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_3, 1), (self.blocks_file_sink_0_0_0_3, 0))
        self.connect((self.blocks_complex_to_float_1_0_3, 0), (self.blocks_file_sink_0_1_3, 0))
        self.connect((self.blocks_complex_to_float_1_0_3_0, 1), (self.blocks_file_sink_0_0_0_3_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_3_0, 0), (self.blocks_file_sink_0_1_3_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_4, 1), (self.blocks_file_sink_0_0_0_4, 0))
        self.connect((self.blocks_complex_to_float_1_0_4, 0), (self.blocks_file_sink_0_1_4, 0))
        self.connect((self.blocks_complex_to_float_1_0_4_0, 1), (self.blocks_file_sink_0_0_0_4_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_4_0, 0), (self.blocks_file_sink_0_1_4_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_5, 1), (self.blocks_file_sink_0_0_0_5, 0))
        self.connect((self.blocks_complex_to_float_1_0_5, 0), (self.blocks_file_sink_0_1_5, 0))
        self.connect((self.blocks_complex_to_float_1_0_5_0, 1), (self.blocks_file_sink_0_0_0_5_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_5_0, 0), (self.blocks_file_sink_0_1_5_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_6, 1), (self.blocks_file_sink_0_0_0_6, 0))
        self.connect((self.blocks_complex_to_float_1_0_6, 0), (self.blocks_file_sink_0_1_6, 0))
        self.connect((self.blocks_complex_to_float_1_0_6_0, 1), (self.blocks_file_sink_0_0_0_6_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_6_0, 0), (self.blocks_file_sink_0_1_6_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_7, 1), (self.blocks_file_sink_0_0_0_7, 0))
        self.connect((self.blocks_complex_to_float_1_0_7, 0), (self.blocks_file_sink_0_1_7, 0))
        self.connect((self.blocks_complex_to_float_1_0_7_0, 1), (self.blocks_file_sink_0_0_0_7_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_7_0, 0), (self.blocks_file_sink_0_1_7_0, 0))
        self.connect((self.blocks_complex_to_float_1_0_8, 1), (self.blocks_file_sink_0_0_0_8, 0))
        self.connect((self.blocks_complex_to_float_1_0_8, 0), (self.blocks_file_sink_0_1_8, 0))
        self.connect((self.blocks_complex_to_float_1_0_9, 1), (self.blocks_file_sink_0_0_0_9, 0))
        self.connect((self.blocks_complex_to_float_1_0_9, 0), (self.blocks_file_sink_0_1_9, 0))
        self.connect((self.blocks_complex_to_float_1_2, 1), (self.blocks_file_sink_0_0_2, 0))
        self.connect((self.blocks_complex_to_float_1_2, 0), (self.blocks_file_sink_0_3, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_stream_mux_3, 3))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_mux_4, 1))
        self.connect((self.blocks_null_source_1, 0), (self.blocks_stream_mux_4, 2))
        self.connect((self.blocks_null_source_1_0, 0), (self.blocks_stream_mux_3, 2))
        self.connect((self.blocks_null_source_1_0_0, 0), (self.blocks_stream_mux_3, 4))
        self.connect((self.blocks_null_source_2, 0), (self.blocks_stream_mux_3, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.txid_correlator_0, 0))
        self.connect((self.blocks_stream_mux_3, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_stream_mux_4, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.txid_head_0_2, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.digital_ofdm_rx_0, 0), (self.txid_data_switch_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_stream_mux_4, 0))
        self.connect((self.preamble_vect, 0), (self.blocks_stream_mux_3, 1))
        self.connect((self.txid_correlator_0, 0), (self.txid_packet_isolator_c_0, 0))
        self.connect((self.txid_data_switch_0, 0), (self.txid_head_0, 0))
        self.connect((self.txid_data_switch_0, 1), (self.txid_head_0_0, 0))
        self.connect((self.txid_data_switch_0, 4), (self.txid_head_0_0_0, 0))
        self.connect((self.txid_data_switch_0, 16), (self.txid_head_0_0_0_0, 0))
        self.connect((self.txid_data_switch_0, 6), (self.txid_head_0_0_1, 0))
        self.connect((self.txid_data_switch_0, 17), (self.txid_head_0_0_1_0, 0))
        self.connect((self.txid_data_switch_0, 7), (self.txid_head_0_0_2, 0))
        self.connect((self.txid_data_switch_0, 18), (self.txid_head_0_0_2_0, 0))
        self.connect((self.txid_data_switch_0, 8), (self.txid_head_0_0_3, 0))
        self.connect((self.txid_data_switch_0, 19), (self.txid_head_0_0_3_0, 0))
        self.connect((self.txid_data_switch_0, 9), (self.txid_head_0_0_4, 0))
        self.connect((self.txid_data_switch_0, 20), (self.txid_head_0_0_4_0, 0))
        self.connect((self.txid_data_switch_0, 10), (self.txid_head_0_0_5, 0))
        self.connect((self.txid_data_switch_0, 2), (self.txid_head_0_0_5_0, 0))
        self.connect((self.txid_data_switch_0, 11), (self.txid_head_0_0_6, 0))
        self.connect((self.txid_data_switch_0, 3), (self.txid_head_0_0_6_0, 0))
        self.connect((self.txid_data_switch_0, 13), (self.txid_head_0_0_7, 0))
        self.connect((self.txid_data_switch_0, 5), (self.txid_head_0_0_7_0, 0))
        self.connect((self.txid_data_switch_0, 12), (self.txid_head_0_0_8, 0))
        self.connect((self.txid_data_switch_0, 15), (self.txid_head_0_0_9, 0))
        self.connect((self.txid_data_switch_0, 14), (self.txid_head_0_1, 0))
        self.connect((self.txid_head_0, 0), (self.blocks_complex_to_float_1, 0))
        self.connect((self.txid_head_0_0, 0), (self.blocks_complex_to_float_1_0, 0))
        self.connect((self.txid_head_0_0_0, 0), (self.blocks_complex_to_float_1_0_0, 0))
        self.connect((self.txid_head_0_0_0_0, 0), (self.blocks_complex_to_float_1_0_0_0, 0))
        self.connect((self.txid_head_0_0_1, 0), (self.blocks_complex_to_float_1_0_1, 0))
        self.connect((self.txid_head_0_0_1_0, 0), (self.blocks_complex_to_float_1_0_1_0, 0))
        self.connect((self.txid_head_0_0_2, 0), (self.blocks_complex_to_float_1_0_2, 0))
        self.connect((self.txid_head_0_0_2_0, 0), (self.blocks_complex_to_float_1_0_2_0, 0))
        self.connect((self.txid_head_0_0_3, 0), (self.blocks_complex_to_float_1_0_3, 0))
        self.connect((self.txid_head_0_0_3_0, 0), (self.blocks_complex_to_float_1_0_3_0, 0))
        self.connect((self.txid_head_0_0_4, 0), (self.blocks_complex_to_float_1_0_4, 0))
        self.connect((self.txid_head_0_0_4_0, 0), (self.blocks_complex_to_float_1_0_4_0, 0))
        self.connect((self.txid_head_0_0_5, 0), (self.blocks_complex_to_float_1_0_5, 0))
        self.connect((self.txid_head_0_0_5_0, 0), (self.blocks_complex_to_float_1_0_5_0, 0))
        self.connect((self.txid_head_0_0_6, 0), (self.blocks_complex_to_float_1_0_6, 0))
        self.connect((self.txid_head_0_0_6_0, 0), (self.blocks_complex_to_float_1_0_6_0, 0))
        self.connect((self.txid_head_0_0_7, 0), (self.blocks_complex_to_float_1_0_7, 0))
        self.connect((self.txid_head_0_0_7_0, 0), (self.blocks_complex_to_float_1_0_7_0, 0))
        self.connect((self.txid_head_0_0_8, 0), (self.blocks_complex_to_float_1_0_8, 0))
        self.connect((self.txid_head_0_0_9, 0), (self.blocks_complex_to_float_1_0_9, 0))
        self.connect((self.txid_head_0_1, 0), (self.blocks_complex_to_float_1_2, 0))
        self.connect((self.txid_head_0_2, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.txid_packet_isolator_c_0, 0), (self.digital_ofdm_rx_0, 0))
        self.connect((self.txid_packet_isolator_c_0, 0), (self.txid_data_switch_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "reciever")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_file_im(self):
        return self.file_im

    def set_file_im(self, file_im):
        self.file_im = file_im
        self.blocks_file_sink_0_0.open(self.file_im+'_0'+'.bin')
        self.blocks_file_sink_0_0_0.open(self.file_im+'_1'+'.bin')
        self.blocks_file_sink_0_0_0_0.open(self.file_im+'_2'+'.bin')
        self.blocks_file_sink_0_0_0_0_0.open(self.file_im+'_13'+'.bin')
        self.blocks_file_sink_0_0_0_1.open(self.file_im+'_3'+'.bin')
        self.blocks_file_sink_0_0_0_1_0.open(self.file_im+'_14'+'.bin')
        self.blocks_file_sink_0_0_0_2.open(self.file_im+'_4'+'.bin')
        self.blocks_file_sink_0_0_0_2_0.open(self.file_im+'_15'+'.bin')
        self.blocks_file_sink_0_0_0_3.open(self.file_im+'_5'+'.bin')
        self.blocks_file_sink_0_0_0_3_0.open(self.file_im+'_16'+'.bin')
        self.blocks_file_sink_0_0_0_4.open(self.file_im+'_6'+'.bin')
        self.blocks_file_sink_0_0_0_4_0.open(self.file_im+'_17'+'.bin')
        self.blocks_file_sink_0_0_0_5.open(self.file_im+'_7'+'.bin')
        self.blocks_file_sink_0_0_0_5_0.open(self.file_im+'_18'+'.bin')
        self.blocks_file_sink_0_0_0_6.open(self.file_im+'_8'+'.bin')
        self.blocks_file_sink_0_0_0_6_0.open(self.file_im+'_19'+'.bin')
        self.blocks_file_sink_0_0_0_7.open(self.file_im+'_9'+'.bin')
        self.blocks_file_sink_0_0_0_7_0.open(self.file_im+'_20'+'.bin')
        self.blocks_file_sink_0_0_0_8.open(self.file_im+'_10'+'.bin')
        self.blocks_file_sink_0_0_0_9.open(self.file_im+'_12'+'.bin')
        self.blocks_file_sink_0_0_2.open(self.file_im+'_11'+'.bin')

    def get_file_re(self):
        return self.file_re

    def set_file_re(self, file_re):
        self.file_re = file_re
        self.blocks_file_sink_0.open(self.file_re+'_0'+'.bin')
        self.blocks_file_sink_0_1.open(self.file_re+'_1'+'.bin')
        self.blocks_file_sink_0_1_0.open(self.file_re+'_2'+'.bin')
        self.blocks_file_sink_0_1_0_0.open(self.file_re+'_13'+'.bin')
        self.blocks_file_sink_0_1_1.open(self.file_re+'_3'+'.bin')
        self.blocks_file_sink_0_1_1_0.open(self.file_re+'_14'+'.bin')
        self.blocks_file_sink_0_1_2.open(self.file_re+'_4'+'.bin')
        self.blocks_file_sink_0_1_2_0.open(self.file_re+'_15'+'.bin')
        self.blocks_file_sink_0_1_3.open(self.file_re+'_5'+'.bin')
        self.blocks_file_sink_0_1_3_0.open(self.file_re+'_16'+'.bin')
        self.blocks_file_sink_0_1_4.open(self.file_re+'_6'+'.bin')
        self.blocks_file_sink_0_1_4_0.open(self.file_re+'_17'+'.bin')
        self.blocks_file_sink_0_1_5.open(self.file_re+'_7'+'.bin')
        self.blocks_file_sink_0_1_5_0.open(self.file_re+'_18'+'.bin')
        self.blocks_file_sink_0_1_6.open(self.file_re+'_8'+'.bin')
        self.blocks_file_sink_0_1_6_0.open(self.file_re+'_19'+'.bin')
        self.blocks_file_sink_0_1_7.open(self.file_re+'_9'+'.bin')
        self.blocks_file_sink_0_1_7_0.open(self.file_re+'_20'+'.bin')
        self.blocks_file_sink_0_1_8.open(self.file_re+'_10'+'.bin')
        self.blocks_file_sink_0_1_9.open(self.file_re+'_12'+'.bin')
        self.blocks_file_sink_0_3.open(self.file_re+'_11'+'.bin')

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

    def get_nb_samples_to_save(self):
        return self.nb_samples_to_save

    def set_nb_samples_to_save(self, nb_samples_to_save):
        self.nb_samples_to_save = nb_samples_to_save
        self.txid_head_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_0_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_1.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_1_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_2.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_2_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_3.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_3_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_4.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_4_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_5.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_5_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_6.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_6_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_7.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_7_0.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_8.set_length(self.nb_samples_to_save)
        self.txid_head_0_0_9.set_length(self.nb_samples_to_save)
        self.txid_head_0_1.set_length(self.nb_samples_to_save)

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

    def get_tx_amount(self):
        return self.tx_amount

    def set_tx_amount(self, tx_amount):
        self.tx_amount = tx_amount

    def get_tx_id(self):
        return self.tx_id

    def set_tx_id(self, tx_id):
        self.tx_id = tx_id
        self.blocks_vector_source_x_0_0_0.set_data((self.tx_id, self.tx_id, self.tx_id, self.tx_id, self.tx_id), [])

    def get_usrp_tx_gain(self):
        return self.usrp_tx_gain

    def set_usrp_tx_gain(self, usrp_tx_gain):
        self.usrp_tx_gain = usrp_tx_gain
        self.iio_pluto_sink_0.set_attenuation(0,80-self.usrp_tx_gain)

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

    def get_usrp_rx_gain(self):
        return self.usrp_rx_gain

    def set_usrp_rx_gain(self, usrp_rx_gain):
        self.usrp_rx_gain = usrp_rx_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.preamble_vect.set_data(self.preamble, [])

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
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
        self.txid_head_0_2.set_length(self.full_header)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.iio_pluto_sink_0.set_frequency(int(self.center_freq))
        self.iio_pluto_source_0.set_frequency(int(self.center_freq))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-I", "--file-im", dest="file_im", type=str, default='enreg_im',
        help="Set file_im [default=%(default)r]")
    parser.add_argument(
        "-R", "--file-re", dest="file_re", type=str, default='enreg_re',
        help="Set file_re [default=%(default)r]")
    parser.add_argument(
        "-f", "--gain-freq", dest="gain_freq", type=eng_float, default=eng_notation.num_to_str(float(2)),
        help="Set gain_frequency [default=%(default)r]")
    parser.add_argument(
        "-r", "--is-noise", dest="is_noise", type=intx, default=0,
        help="Set is_noise [default=%(default)r]")
    parser.add_argument(
        "--is-random-source", dest="is_random_source", type=intx, default=0,
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
        "-S", "--nb-samples-to-save", dest="nb_samples_to_save", type=intx, default=(600*(50000 + 2000)),
        help="Set nb_samples_to_save [default=%(default)r]")
    parser.add_argument(
        "-L", "--packet-len", dest="packet_len", type=intx, default=400,
        help="Set packet_len [default=%(default)r]")
    parser.add_argument(
        "-P", "--port", dest="port", type=intx, default=3580,
        help="Set port_number [default=%(default)r]")
    parser.add_argument(
        "-s", "--space-between-packets", dest="space_between_packets", type=intx, default=200,
        help="Set space_between_packets [default=%(default)r]")
    parser.add_argument(
        "-T", "--tx-amount", dest="tx_amount", type=intx, default=21,
        help="Set tx_amount [default=%(default)r]")
    parser.add_argument(
        "--tx-id", dest="tx_id", type=intx, default=0,
        help="Set tx_id [default=%(default)r]")
    parser.add_argument(
        "-G", "--usrp-tx-gain", dest="usrp_tx_gain", type=intx, default=3,
        help="Set gain [default=%(default)r]")
    return parser


def main(top_block_cls=reciever, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(file_im=options.file_im, file_re=options.file_re, gain_freq=options.gain_freq, is_noise=options.is_noise, is_random_source=options.is_random_source, max_gain=options.max_gain, min_gain=options.min_gain, nb_packets=options.nb_packets, nb_samples_to_save=options.nb_samples_to_save, packet_len=options.packet_len, port=options.port, space_between_packets=options.space_between_packets, tx_amount=options.tx_amount, tx_id=options.tx_id, usrp_tx_gain=options.usrp_tx_gain)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
