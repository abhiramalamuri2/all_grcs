#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from packaging.version import Version as StrictVersion
import ctypes
import sys
import signal
import time
from PyQt5 import Qt
from gnuradio import gr, blocks, analog, uhd
from gnuradio import qtgui

if __name__ == '__main__':
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary(' libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

class usrpsimple(gr.top_block, Qt.QWidget):
    def __init__(self):
        gr.top_block.__init__(self, "USRP Simple Example", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("USRP Simple Example")
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

        self.settings = Qt.QSettings("GNU Radio", "usrpsimple")

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
        self.samp_rate = 30e6  # Sample rate
        self.last_sample_count = 0  # Stores the sample count from the previous interval
        self.last_time = time.time()
        self.threshold = 0.01  # Signal energy threshold to detect valid signal

        ##################################################
        # Blocks
        ##################################################
        # USRP source (receiving data)
        self.uhd_usrp_source = uhd.usrp_source(
            ",".join(('', '')),
            uhd.stream_args(
                cpu_format="fc32",
                channels=list(range(1)),
            ),
        )
        self.uhd_usrp_source.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source.set_center_freq(20e6, 0)
        self.uhd_usrp_source.set_antenna('A', 0)
        self.uhd_usrp_source.set_bandwidth(1e6, 0)
        self.uhd_usrp_source.set_gain(70, 0)

        # USRP sink (transmitting data)
        self.uhd_usrp_sink = uhd.usrp_sink(
            ",".join(('', '')),
            uhd.stream_args(
                cpu_format="fc32",
                channels=list(range(1)),
            ),
        )
        self.uhd_usrp_sink.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink.set_center_freq(20e6, 0)
        self.uhd_usrp_sink.set_antenna('A', 0)
        self.uhd_usrp_sink.set_bandwidth(1e6, 0)
        self.uhd_usrp_sink.set_gain(70, 0)

        # Probe signal to measure the number of samples received
        self.blocks_probe = blocks.probe_signal_c()

        # Signal energy detection: convert complex to magnitude squared
        self.blocks_complex_to_mag_squared = blocks.complex_to_mag_squared()

        # Moving average block to smooth the energy signal
        self.blocks_moving_average = blocks.moving_average_ff(1000, 1.0 / 1000)

        # Another probe signal to monitor the energy level
        self.blocks_probe_energy = blocks.probe_signal_f()

        # Analog signal source (for transmission example)
        self.analog_sig_source = analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source, 0), (self.uhd_usrp_sink, 0))
        self.connect((self.uhd_usrp_source, 0), (self.blocks_probe, 0))
        self.connect((self.uhd_usrp_source, 0), (self.blocks_complex_to_mag_squared, 0))
        self.connect((self.blocks_complex_to_mag_squared, 0), (self.blocks_moving_average, 0))
        self.connect((self.blocks_moving_average, 0), (self.blocks_probe_energy, 0))

        # Timer to print data rate every second
        self.data_rate_timer = Qt.QTimer()
        self.data_rate_timer.timeout.connect(self.print_data_rate)
        self.data_rate_timer.start(1000)  # Timer interval in milliseconds

    def print_data_rate(self):
        # Get the current sample count
        current_sample_count = self.blocks_probe.nitems_read(0)
        current_time = time.time()

        # Get the current signal energy level
        signal_energy = self.blocks_probe_energy.level()

        # Only calculate and print data rate if signal energy is above the threshold
        if signal_energy > self.threshold:
            # Calculate how many samples were received in the last second
            samples_received = current_sample_count - self.last_sample_count
            elapsed_time = current_time - self.last_time

            # Update last_sample_count and last_time for the next interval
            self.last_sample_count = current_sample_count
            self.last_time = current_time

            # Calculate data rate for the last second
            data_rate = (samples_received / elapsed_time) / 1e6 * 8  # Convert to Mbps
            print(f"Received Data Rate: {data_rate:.2f} Mbps")
        else:
            print("No valid signal detected.")

    def closeEvent(self, event):
        self.data_rate_timer.stop()  # Stop the data rate timer
        self.stop()
        self.wait()
        event.accept()

def main(top_block_cls=usrpsimple, options=None):
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
    signal.signal(signal.SIGNTERM, sig_handler)

    qapp.exec_()

if __name__ == '__main__':
    main()