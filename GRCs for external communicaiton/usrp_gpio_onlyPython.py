#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


def snipfcn_snippet_0(self):
    import uhd
    import time

    # Initialize the USRP device
    usrp = uhd.usrp.MultiUSRP()

    # Choose an available GPIO bank, such as FP0A
    gpio_bank = "FP0A"

    # Configure GPIO direction
    direction_mask = 0x01  # Set GPIO pin 0 as output
    usrp.set_gpio_attr(gpio_bank, "DDR", direction_mask, direction_mask, 0)  # Use radio index 0

    # Commenting out the "OUT_EN" line to see if it's necessary
    # output_enable_mask = 0x01  # Enable GPIO pin 0 for output
    # usrp.set_gpio_attr(gpio_bank, "OUT_EN", output_enable_mask, output_enable_mask, 0)  # Use radio index 0

    # Infinite loop to toggle GPIO high and low
    try:
        while True:
            # Set the GPIO pin to logic high (1)
            usrp.set_gpio_attr(gpio_bank, "OUT", 0x01, 0x01, 0)  # Use radio index 0
            print("GPIO HIGH")
            time.sleep(1)

            # Set the GPIO pin to logic low (0)
            usrp.set_gpio_attr(gpio_bank, "OUT", 0x00, 0x01, 0)  # Use radio index 0
            print("GPIO LOW")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

from gnuradio import qtgui

class usrp_gpio(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "usrp_gpio")

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
        self.samp_rate = samp_rate = 32000



    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_gpio")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=usrp_gpio, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
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
