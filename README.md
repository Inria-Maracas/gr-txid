gr-txid

Set of OOT blocks used to generate the datasets in the paper "Transmitter Classification With Supervised Deep Learning" in the FIT/CorteXlab.


## The what?

This module was developped to be used in the [FIT/CorteXlab](http://www.cortexlab.fr/) platform.
This platform is a designed a a software defined radio tesbed and consists of about 40 SDR nodes (USRPs and PicoSDRs) inside a shielded anechoic chamber for testing of radio designs without interferences from the outside world and without infringing on licences bands, between 400Mhz and 4GHz.

The module provides gnuradio blocks that helps in generating labeled datasets for transmitter classification learning.

## Blocks description

#### UDP trigger
Python block that listens to an UDP port and forwards the first gnuradio asynchronous message received each time an UDP packet arrives containing the specified ID.
It is useful when multiple gnuradio applications are running at the same time to prevent interferences.
It's designed to work with a scheduler program (included in the examples folder) that selects one instance and sends a packet to it, containing the ID of that instance.

#### Data switch
Python block
This block takes the output of an ofdm packet decoder to get the ID of a received packet and uses it to transfer the payload contained in the packet present in the second input towards the proper output port.
The block is designed to work on data containing both the undecoded ofdm header and the payload, so it can dump the samples corresponding to the header and only forward the payload.
More precisely, it will dump the first <header size> samples and forward the next <payload size> samples.
To be able to cope with packet losses at the ofdm receiver, the inputs need to contain a tag at every beginning of packet, named header_start and with an increasing index. This is provided by the packet isolator block.
On top of forwarding payloads to the proper output, the block can also send it in a UDP packet over the network for online classification.

#### Head
C++ block
Slight modification of the stock block of the same name to allow for non blocking operation.
When activated, and when the block reaches its set limit of forwarded samples, the following samples are consumed and destroyed, instead of piling up, filling the buffers and stopping processing upstream.

#### Correlator
C++ block
Slight modification of the standard block.
Here, the correlation values are used compared to the average power of the signal.

#### Packet isolator
C++ block
Uses the output of a correlator block.
Looks for correlation value tags in the input stream. The maximum value over a certain window size is selected as the correlation peak.
From this point, <preamble length> samples are dropped and the next <payload length> samples are forwarded.
A tag is placed at the beginning of each forwarded chunk, with an increasing index. 




## Usage with FIT/CorteXlab
- Register to the [platform](https://wiki.cortexlab.fr/doku.php?id=start) and get familiar with it
- Clone this repository somewhere in your airlock home
- Create a build directory in the repository and, from there, build it (cf next section)
- Book the testbed
- Go to the example directory and modify the scenario, scheduler, create_folder and/or generateData files as needed to get the desired scenario
- Run './generateData.sh'



## How to build for use in a FIT/CorteXlab task:
More info in : [GNU Radio Wiki](https://wiki.cortexlab.fr/doku.php?id=embedding_oot_modules_or_custom_libraries_binaries_in_minus_scenario)
````
cmake -DCMAKE_INSTALL_PREFIX=/home/cxlbuser/tasks/task ..
make
make DESTDIR=/<locationofthisfolder>/examples/src/tmp install
mv /<locationofthisfolder>/examples/src/tmp/home/cxlbuser/tasks/task/* /<locationofthisfolder>/examples/src/
rm -rf /<locationofthisfolder>/examples/src/tmp
````
