find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_LORA_SDR gnuradio-lora_sdr_fmcw_0)

FIND_PATH(
    GR_LORA_SDR_INCLUDE_DIRS
    NAMES gnuradio/lora_sdr_fmcw_0/api.h
    HINTS $ENV{LORA_SDR_DIR}/include
        ${PC_LORA_SDR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_LORA_SDR_LIBRARIES
    NAMES gnuradio-lora_sdr_fmcw_0
    HINTS $ENV{LORA_SDR_DIR}/lib
        ${PC_LORA_SDR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-lora_sdr_fmcw_0Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_LORA_SDR DEFAULT_MSG GR_LORA_SDR_LIBRARIES GR_LORA_SDR_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_LORA_SDR_LIBRARIES GR_LORA_SDR_INCLUDE_DIRS)
