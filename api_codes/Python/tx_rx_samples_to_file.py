#!/usr/bin/env python3
#
# Copyright 2017-2018 Ettus Research, a National Instruments Company
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# python3 tx_rx_samples_to_file.py -a "addr=192.168.10.2" -o output.dat -w sine -f 19e6 -r 10e6 -d 5 -c 0 -g 12 --wave-freq 1e4 --wave-ampl 0.3


# Run this for the best waveform
# python3 tx_rx_samples_to_file.py -a "addr=192.168.10.2" -o output.dat -w sine -f 19e6 -r 25000 -d 5 -c 0 -g 12 --wave-freq 1000 --wave-ampl 0.3
"""
RX samples to file using Python API and TX samples based on input arguments
"""

import argparse
import numpy as np
import uhd
import time

WAVEFORMS = {
    "sine": lambda n, tone_offset, rate: np.exp(n * 2j * np.pi * tone_offset / rate),
    "square": lambda n, tone_offset, rate: np.sign(WAVEFORMS["sine"](n, tone_offset, rate)),
    "const": lambda n, tone_offset, rate: 1 + 1j,
    "ramp": lambda n, tone_offset, rate:
            2*(n*(tone_offset/rate) - np.floor(float(0.5 + n*(tone_offset/rate))))
}

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument("-o", "--output-file", type=str, required=True)
    parser.add_argument(
        "-w", "--waveform", default="sine", choices=WAVEFORMS.keys(), type=str)
    parser.add_argument("-f", "--freq", type=float, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("--wave-freq", default=1e4, type=float)
    parser.add_argument("--wave-ampl", default=0.3, type=float)
    parser.add_argument("-n", "--numpy", default=False, action="store_true",
                        help="Save output file in NumPy format (default: No)")
    return parser.parse_args()
    
def main():
    """RX samples and write to file and TX samples based on input arguments"""
    args = parse_args()
    usrp = uhd.usrp.MultiUSRP(args.args)
    num_samps = int(np.ceil(args.duration*args.rate))
    
    if not isinstance(args.channels, list):
        args.channels = [args.channels]    
    
    data = np.array(
        list(map(lambda n: args.wave_ampl * WAVEFORMS[args.waveform](n, args.wave_freq, args.rate),
                 np.arange(
                     int(10 * np.floor(args.rate / args.wave_freq)),
                     dtype=np.complex64))),
        dtype=np.complex64)  # One period

    usrp.send_waveform(data, args.duration, args.freq, args.rate,
                       args.channels, args.gain)

    #time.sleep(1)

    samps = usrp.recv_num_samps(num_samps, args.freq, args.rate, args.channels, args.gain)
    samps = samps[0:1000]
    with open(args.output_file, 'wb') as out_file:
        if args.numpy:
            np.save(out_file, samps, allow_pickle=False, fix_imports=False)
        else:
            samps.tofile(out_file)

if __name__ == "__main__":
    main()
