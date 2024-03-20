# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT txid_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT txid_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND txid_python_files
    head_python.cc
    packet_isolator_c_python.cc
    packet_header_ofdm_python.cc
    correlator_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(txid
   ../../..
   gr::txid
   "${txid_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET txid_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:txid_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/txid/
)

install(TARGETS txid_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/txid COMPONENT pythonapi)
