find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_TXID gnuradio-txid)

FIND_PATH(
    GR_TXID_INCLUDE_DIRS
    NAMES gnuradio/txid/api.h
    HINTS $ENV{TXID_DIR}/include
        ${PC_TXID_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_TXID_LIBRARIES
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

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-txidTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_TXID DEFAULT_MSG GR_TXID_LIBRARIES GR_TXID_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_TXID_LIBRARIES GR_TXID_INCLUDE_DIRS)
