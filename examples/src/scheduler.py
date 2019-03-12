
import socket
import time
import numpy as np

# addressing information of target
IPADDR = '127.0.0.1'
PORTNUM = 3580
ip_base = 'mnode'

# enter the data content of the UDP packet as hex
PACKETDATA = np.ones(1, dtype=np.uint8)*0

# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

SLEEP_TIME=0.001

nodes = [3, 4, 35, 7, 8, 9, 13, 14, 16, 17, 18, 23, 24, 25, 27, 28, 32, 33, 34, 37, 38] #Mono Rx
# nodes = [6, 4, 35, 7, 8, 9, 13, 14, 16, 17, 18, 23, 24, 25, 27, 28, 32, 33, 34, 37, 38] #Multi Rx

time.sleep(1)
while True:
    #Wait a bit to sent next order
    time.sleep(SLEEP_TIME)

    #Select the next sender (Random order to reduce issues with packet losses)
    node_index = np.random.randint(len(nodes))
    node = nodes[node_index]

    PACKETDATA = np.uint8(node_index)
    IPADDR = ip_base+str(node)

    try:
        # send the command
        s.sendto(PACKETDATA, (IPADDR, PORTNUM))
    except:
        pass

    #Let's do it again


# close the socket
s.close()
