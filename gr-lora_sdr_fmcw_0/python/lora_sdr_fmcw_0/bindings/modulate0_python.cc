#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gnuradio/lora_sdr_fmcw_0/modulate0.h>
namespace py = pybind11;
void bind_modulate0(py::module& m)
{
    using modulate0 = ::gr::lora_sdr_fmcw_0::modulate0;
    py::class_<modulate0, gr::block, gr::basic_block, std::shared_ptr<modulate0>>(m, "modulate0", "")
        .def(py::init(&modulate0::make),
             py::arg("sf"), py::arg("samp_rate"), py::arg("bw"),
             py::arg("sync_words"), py::arg("inter_frame_padd"), py::arg("preamble_len"),
             py::arg("zero_preamble_chirps") = 0, "");
}
