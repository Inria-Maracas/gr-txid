#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Cyrille Morin.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#



from gnuradio import gr
from gnuradio import txid
from gnuradio import blocks

class record_payload(gr.hier_block2):
    """
    docstring for block record_payload
    """
    def __init__(self, tx_amount=21, base_filename="enreg", header_size=379, payload_size=600, to_server=False, server_ip='127.0.0.1', server_port=3581, payloads_to_save=50000):
        gr.hier_block2.__init__(self,
            "record_payload",
            gr.io_signature.make2(2, 2, gr.sizeof_char, gr.sizeof_gr_complex),  # Input signature
            gr.io_signature(0, 0, 0)) # Output signature

        samples_to_save = payloads_to_save * payload_size

        # Define blocks and connect them

        self.header_switch = txid.data_switch(tx_amount, header_size, payload_size, to_server, server_ip, server_port)
        self.connect((self, 0), (self.header_switch, 0))
        self.connect((self, 1), (self.header_switch, 1))

        self.block_list = []
    
        for i in range(tx_amount):
            tmp_head = txid.head(gr.sizeof_gr_complex, samples_to_save, False)
            tmp_convert = blocks.complex_to_float(1)
            tmp_re_sink = blocks.file_sink(gr.sizeof_float, base_filename+ f'_re_{i:02d}.bin', False)
            tmp_re_sink.set_unbuffered(False)
            tmp_im_sink = blocks.file_sink(gr.sizeof_float, base_filename+ f'_im_{i:02d}.bin', False)
            tmp_im_sink.set_unbuffered(False)
            self.connect((self.header_switch, i), tmp_head, tmp_convert)
            self.connect((tmp_convert, 0), tmp_re_sink)
            self.connect((tmp_convert, 1), tmp_im_sink)
            self.block_list.append([tmp_head, tmp_convert, tmp_re_sink, tmp_im_sink])
