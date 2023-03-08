#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-n', '--tx_nodes', help='List of transmitting nodes', 
                    type=lambda s: [int(item) for item in s.split(',')])
parser.add_argument('-s', '--tx_freq', help='Frequency of new packet transmission', type=float, default=0.001)
parser.add_argument('-p', dest="port_num", help="Port to send paquets to", type=int, default=3580)
args = parser.parse_args()

nodes = args.tx_nodes

# addressing information of target
IPADDR = '127.0.0.1'
PORTNUM = args.port_num
ip_base = 'mnode'

# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

SLEEP_TIME=args.tx_freq

# nodes = [3, 4, 35, 7, 8, 9, 13, 14, 16, 17, 18, 23, 24, 25, 27, 28, 32, 33, 34, 37, 38] #Mono Rx
# nodes = [6, 4, 35, 7, 8, 9, 13, 14, 16, 17, 18, 23, 24, 25, 27, 28, 32, 33, 34, 37, 38] #Multi Rx

time.sleep(1)
while True:

    #Select the next sender (Random order to reduce issues with packet losses)
    node_index = np.random.randint(len(nodes))
    node = nodes[node_index]

    PACKETDATA = np.uint8(node_index)
    # IPADDR = ip_base+str(node)

    try:
        # send the command
        s.sendto(PACKETDATA, (IPADDR, PORTNUM))
    except:
        pass

    #Wait a bit to sent next order
    time.sleep(SLEEP_TIME)
    #Let's do it again


# close the socket
s.close()
