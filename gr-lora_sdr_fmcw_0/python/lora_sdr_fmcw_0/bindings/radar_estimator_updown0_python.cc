/* -*- c++ -*- */
#include <pybind11/pybind11.h>
#include <gnuradio/lora_sdr_fmcw_0/radar_estimator_updown0.h>

namespace py = pybind11;

void bind_radar_estimator_updown0(py::module& m)
{
    using radar_estimator_updown0 = ::gr::lora_sdr_fmcw_0::radar_estimator_updown0;

    py::class_<radar_estimator_updown0,
               gr::block,
               gr::basic_block,
               std::shared_ptr<radar_estimator_updown0>>(m, "radar_estimator_updown0", "")
        .def(py::init(&radar_estimator_updown0::make),
             py::arg("samp_rate"),
             py::arg("center_freq"),
             py::arg("sweep_freq"),
             py::arg("samp_up"),
             py::arg("samp_down"),
             py::arg("push_power") = false,
             "");
}
