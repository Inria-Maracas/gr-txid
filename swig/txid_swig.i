/* -*- c++ -*- */

#define TXID_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "txid_swig_doc.i"

%{
#include "txid/correlator.h"
#include "txid/head.h"
#include "txid/packet_isolator_c.h"
%}


%include "txid/correlator.h"
GR_SWIG_BLOCK_MAGIC2(txid, correlator);
%include "txid/head.h"
GR_SWIG_BLOCK_MAGIC2(txid, head);
%include "txid/packet_isolator_c.h"
GR_SWIG_BLOCK_MAGIC2(txid, packet_isolator_c);
