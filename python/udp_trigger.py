#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Cyrille Morin.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
import pmt
import struct
from gnuradio import gr
import socket
import threading

class udp_trigger(gr.sync_block):
    """
    Triggers the transmission of a previously received message upon reception of a udp packet containing the right tx_number
    """
    def __init__(self, tx_number=0,ip_addr='127.0.0.1', port=3500):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='UDP trigger',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.tx_number = tx_number
        self.ip_addr = ip_addr
        self.port = port
        self.message_port_register_out(pmt.intern("out"))
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)
        self.message_buffer = None
        self.once = False
        print("Init")
        # self.socket_thread = threading.Thread(target=self.handle_packet)
        # self.socket_thread.daemon = True
        # self.socket_thread.start()


    def handle_msg(self, msg):
        if self.once:
            return
        self.once = True
        self.message_buffer = msg
        print(msg)
        print("Thread")
        # initialize a socket, think of it as a cable
        # SOCK_DGRAM specifies that this is UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.s.bind((self.ip_addr,self.port))
        print("Listening")
        while 1: # Reception loop
            data = self.s.recv(1024)
            number = struct.unpack('B',data)[0]
            if number != self.tx_number:
                print("Wrong target")
                continue
            if self.message_buffer is not None:
                print("sending",number)
                self.message_port_pub(pmt.intern("out"),self.message_buffer)



    def __exit__(self, exc_type, exc_value, traceback):
        # print("Exit")
        self.s.close() #Close socket

    # def handle_packet(self):
    #     pass


    def work(self, input_items, output_items):
        """example: multiply with constant"""

        return 0
