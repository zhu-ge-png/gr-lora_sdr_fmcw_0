/* -*- c++ -*- */
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gnuradio/lora_sdr_fmcw_0/frame_sync0.h>

namespace py = pybind11;

void bind_frame_sync0(py::module& m)
{
    using frame_sync0 = ::gr::lora_sdr_fmcw_0::frame_sync0;

    py::class_<frame_sync0, gr::block, gr::basic_block, std::shared_ptr<frame_sync0>>(m, "frame_sync0", "")
        .def(py::init(&frame_sync0::make),
             py::arg("center_freq"),
             py::arg("bandwidth"),
             py::arg("sf"),
             py::arg("impl_head"),
             py::arg("sync_word"),
             py::arg("os_factor"),
             py::arg("preamble_len"),
             py::arg("detect_corr_threshold") = 0.45f,
             py::arg("fmcw_preamble_len") = -1,
             "")
        .def("set_detect_corr_threshold",
             &frame_sync0::set_detect_corr_threshold,
             py::arg("detect_corr_threshold"));
}
