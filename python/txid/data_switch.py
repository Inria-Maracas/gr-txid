#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Cyrille Morin.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import pmt
import time
import socket
from gnuradio import gr

class data_switch(gr.basic_block):
    """
    Receives the Tx ID
    """
    def __init__(self, tx_amount=2, header_size = 380, payload_size= 600, to_network = False, address = "127.0.0.1", port = 3581):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        out_sig = []
        for i in range(tx_amount):
            out_sig += [np.complex64]
        gr.basic_block.__init__(
            self,
            name='Header based switch',   # will show up in GRC
            in_sig=[np.uint8, np.complex64],
            out_sig=out_sig
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.tx_amount = tx_amount
        self.header_size = header_size
        self.payload_size = payload_size
        self.block_size = header_size+payload_size
        self.set_output_multiple(self.payload_size)
        self.set_tag_propagation_policy(0)
        self.header_byte_length = 5
        self.last_called = float("inf")
        self.max_wait_time = 0.01

        self.to_network = to_network
        if self.to_network:
            # initialize a socket, think of it as a cable
            # SOCK_DGRAM specifies that this is UDP
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            self.addr = address
            self.port = port

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        ninput_items_required[0] = 0#self.header_byte_length
        ninput_items_required[1] = self.block_size

    def vote(self, data):
        """Returns the most present value in the input array"""
        values = np.zeros(self.tx_amount)
        for i in range(len(data)):
            values[data[i]] += 1
        return np.argmax(values)


    def general_work(self, input_items, output_items):
        """example: multiply with constant"""
        # print("Work",len(input_items[0]), len(input_items[1]) )

        # Get tags to synchronise the two streams
        tags0 = self.get_tags_in_window(0,  0 , self.header_byte_length, pmt.intern("header_start"))
        tags1 = self.get_tags_in_window(1,  0 , self.block_size, pmt.intern("header_start"))
        if len(input_items[0]) < self.header_byte_length:
            #print("Not enough input")
            if time.clock() - self.last_called > self.max_wait_time:
                # print("Wait too long, consuming")
                self.consume(1, self.block_size)
                self.last_called = float("inf")
            if self.last_called == float("inf"):
                self.last_called = time.clock()
            time.sleep(0.001)
            return 0
        self.last_called = float("inf")
        if len(tags0)==0:
            # print("No decoded tags")
            self.consume(0,self.header_byte_length)
            #self.consume(1, self.block_size)
            return 0
        if len(tags1)==0:
            # print("No data tags")
            self.consume(1, self.block_size)
            return 0

        print(pmt.to_python(tags0[0].value), pmt.to_python(tags1[0].value))
        if pmt.to_python(tags0[0].value) < pmt.to_python(tags1[0].value):
            # print("Decoded late")
            self.consume(0,self.header_byte_length)
            return 0
        if pmt.to_python(tags0[0].value) > pmt.to_python(tags1[0].value):
            # print("Decoded early")
            self.consume(1, self.block_size* (pmt.to_python(tags0[0].value)-pmt.to_python(tags1[0].value)))
            return 0

        tx_id = self.vote(input_items[0][:self.header_byte_length])
        if tx_id<self.tx_amount:
            output_items[tx_id][:self.payload_size] = input_items[1][self.header_size:self.block_size]
            #output_items[0][0] = 1
            self.produce(int(tx_id),self.payload_size)
            self.add_item_tag(int(tx_id), self.nitems_written(int(tx_id)), pmt.intern("header_start"), pmt.to_pmt(0))

            if self.to_network:
                PACKETDATA = np.uint8(tx_id).tostring() + (input_items[1][self.header_size:self.block_size].real).tostring() + (input_items[1][self.header_size:self.block_size].imag).tostring()
                self.s.sendto(PACKETDATA, (self.addr, self.port))
        else:
            print("Txid too big")

        self.consume(0,self.header_byte_length)
        self.consume(1, self.block_size)
        return 0


