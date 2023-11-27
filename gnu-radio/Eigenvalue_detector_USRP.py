#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: Stream
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Eigenvalue_detector_USRP_epy_block_1_0 as epy_block_1_0  # embedded python block



from gnuradio import qtgui

class Eigenvalue_detector_USRP(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Eigenvalue_detector_USRP")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e6
        self.correction = correction = 1
        self.channel_selector = channel_selector = 1
        self.center_freq = center_freq = 90e6
        self.amplitude_noise = amplitude_noise = 0
        self.Threshold_range = Threshold_range = 0
        self.Number_of_channels = Number_of_channels = 10

        ##################################################
        # Blocks
        ##################################################
        self._Number_of_channels_range = Range(1, 20, 1, 10, 200)
        self._Number_of_channels_win = RangeWidget(self._Number_of_channels_range, self.set_Number_of_channels, "'Number_of_channels'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Number_of_channels_win)
        self._correction_range = Range(1, 30, 0.1, 1, 200)
        self._correction_win = RangeWidget(self._correction_range, self.set_correction, "'correction'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._correction_win)
        self._channel_selector_range = Range(0, Number_of_channels-1, 1, 1, 200)
        self._channel_selector_win = RangeWidget(self._channel_selector_range, self.set_channel_selector, "'channel_selector'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._channel_selector_win)
        self._center_freq_range = Range(80e6, 100e6, 1e6, 90e6, 200)
        self._center_freq_win = RangeWidget(self._center_freq_range, self.set_center_freq, "'center_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_freq_win)
        self._amplitude_noise_range = Range(0, 0.1, 0.001, 0, 200)
        self._amplitude_noise_win = RangeWidget(self._amplitude_noise_range, self.set_amplitude_noise, "'amplitude_noise'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._amplitude_noise_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(50, 0)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            16384,
            (center_freq-samp_rate/2)/(1e6),
            (samp_rate/(1e6))/16384,
            "Frequency (MHz)",
            "",
            "",
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.05)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 2)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['Channel acitivation', 'FFT', '', '', '',
            '', '', '', '', '']
        widths = [4, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["red", "blue", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            8192, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/20)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.fft_vxx_0 = fft.fft_vcc(2**14, True, window.blackmanharris(2**14), True, 1)
        self.epy_block_1_0 = epy_block_1_0.blk(vectorSize=16384, Pfa=0.05, Smooth_fact=30, Threshold_corr=correction, sampling_rate=samp_rate, num_channels=Number_of_channels, channel=channel_selector, noise_amplitude=0.01)
        self.blocks_stream_to_vector_decimator_0 = blocks.stream_to_vector_decimator(
            item_size=gr.sizeof_gr_complex,
            sample_rate=samp_rate,
            vec_rate=10,
            vec_len=2**14)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*16384)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 2**14, 0)
        self.blocks_message_debug_0_0 = blocks.message_debug(True)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(2**14)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, amplitude_noise, 0)
        self._Threshold_range_range = Range(0, 50, 10, 0, 200)
        self._Threshold_range_win = RangeWidget(self._Threshold_range_range, self.set_Threshold_range, "'Threshold_range'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Threshold_range_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_decimator_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.blocks_stream_to_vector_decimator_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.blocks_stream_to_vector_decimator_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.epy_block_1_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_1_0, 1), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Eigenvalue_detector_USRP")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_stream_to_vector_decimator_0.set_sample_rate(self.samp_rate)
        self.epy_block_1_0.sampling_rate = self.samp_rate
        self.qtgui_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis((self.center_freq-self.samp_rate/2)/(1e6), (self.samp_rate/(1e6))/16384)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 0)

    def get_correction(self):
        return self.correction

    def set_correction(self, correction):
        self.correction = correction
        self.epy_block_1_0.Threshold_corr = self.correction

    def get_channel_selector(self):
        return self.channel_selector

    def set_channel_selector(self, channel_selector):
        self.channel_selector = channel_selector
        self.epy_block_1_0.channel = self.channel_selector

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis((self.center_freq-self.samp_rate/2)/(1e6), (self.samp_rate/(1e6))/16384)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_amplitude_noise(self):
        return self.amplitude_noise

    def set_amplitude_noise(self, amplitude_noise):
        self.amplitude_noise = amplitude_noise
        self.analog_noise_source_x_0.set_amplitude(self.amplitude_noise)

    def get_Threshold_range(self):
        return self.Threshold_range

    def set_Threshold_range(self, Threshold_range):
        self.Threshold_range = Threshold_range

    def get_Number_of_channels(self):
        return self.Number_of_channels

    def set_Number_of_channels(self, Number_of_channels):
        self.Number_of_channels = Number_of_channels
        self.epy_block_1_0.num_channels = self.Number_of_channels




def main(top_block_cls=Eigenvalue_detector_USRP, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
