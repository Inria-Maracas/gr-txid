FROM m1mbert/cxlb-gnuradio-3.10:1.2

SHELL [ "/bin/bash", "-lc"  ]
RUN git clone -b port3.10  https://github.com/Inria-Maracas/gr-txid.git
RUN cd gr-txid && mkdir build
RUN cd gr-txid/build && cmake ..
RUN cd gr-txid/build && make install && ldconfig

# ENTRYPOINT [ "/bin/bash", "-l", ";" ]
# CMD [ "/bin/bash", "-lc", "/usr/sbin/sshd -p 2222 -D" ]
# CMD [ "/bin/bash", "-lc", "/usr/sbin/sshd", "-p", "2222", "-D" ]