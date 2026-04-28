/* -*- c++ -*- */
#include <pybind11/pybind11.h>
#include <gnuradio/lora_sdr_fmcw_0/radar_rx0.h>

namespace py = pybind11;

void bind_radar_rx0(py::module& m)
{
    using radar_rx0 = ::gr::lora_sdr_fmcw_0::radar_rx0;

    py::class_<radar_rx0, gr::block, gr::basic_block, std::shared_ptr<radar_rx0>>(
        m, "radar_rx0", "")
        .def(py::init(&radar_rx0::make),
             py::arg("bandwidth"),
             py::arg("sf"),
             py::arg("os_factor") = 4,
             py::arg("corr_threshold") = 0.45f,
             py::arg("len_tag_key") = "radar_len",
             "")
        .def("set_corr_threshold",
             &radar_rx0::set_corr_threshold,
             py::arg("corr_threshold"));
}
