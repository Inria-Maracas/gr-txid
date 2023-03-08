FROM m1mbert/cxlb-gnuradio-3.10:1.2


RUN git clone -b port3.10  https://github.com/Inria-Maracas/gr-txid.git
RUN cd gr-txid && mkdir build
RUN . /etc/profile.d/cxlb-toolchain-user-conf.sh && cd gr-txid/build && cmake ..
RUN cd gr-txid/build && make install
RUN cd


