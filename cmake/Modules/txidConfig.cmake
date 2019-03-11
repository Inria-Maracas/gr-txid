INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_TXID txid)

FIND_PATH(
    TXID_INCLUDE_DIRS
    NAMES txid/api.h
    HINTS $ENV{TXID_DIR}/include
        ${PC_TXID_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TXID_LIBRARIES
    NAMES gnuradio-txid
    HINTS $ENV{TXID_DIR}/lib
        ${PC_TXID_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TXID DEFAULT_MSG TXID_LIBRARIES TXID_INCLUDE_DIRS)
MARK_AS_ADVANCED(TXID_LIBRARIES TXID_INCLUDE_DIRS)

