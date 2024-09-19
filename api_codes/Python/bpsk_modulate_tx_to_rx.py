#!/usr/bin/env python3
#
# Copyright 2017-2018 Ettus Research, a National Instruments Company
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
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

def text_to_bits(text):
    """Convert text to binary."""
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bitstring):
    """Convert bitstring back to text."""
    chars = [bitstring[i:i+8] for i in range(0, len(bitstring), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def bpsk_modulate(bitstring):
    """Modulate a bitstring using BPSK."""
    return np.array([1 if bit == '1' else -1 for bit in bitstring], dtype=np.float32)

def bpsk_demodulate(samples):
    """Demodulate BPSK symbols back into bits."""
    return ''.join(['1' if sample.real > 0 else '0' for sample in samples])

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument("-o", "--output-file", type=str, required=True)
    parser.add_argument("-w", "--waveform", default="sine", choices=WAVEFORMS.keys(), type=str)
    parser.add_argument("-f", "--freq", type=float, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("--wave-freq", default=1e4, type=float)
    parser.add_argument("--wave-ampl", default=0.3, type=float)
    parser.add_argument("--text", default="Hello World", type=str, help="Text to transmit")
    parser.add_argument("-n", "--numpy", default=False, action="store_true",
                        help="Save output file in NumPy format (default: No)")
    return parser.parse_args()

def main():
    """RX samples and write to file and TX samples based on input arguments"""
    args = parse_args()
    usrp = uhd.usrp.MultiUSRP(args.args)
    num_samps = int(np.ceil(args.duration * args.rate))
    
    if not isinstance(args.channels, list):
        args.channels = [args.channels]

    # Convert text to binary and modulate using BPSK
    bitstring = text_to_bits(args.text)
    bpsk_symbols = bpsk_modulate(bitstring)

    # Resample to match USRP rate
    data = np.tile(bpsk_symbols, int(np.ceil(num_samps / len(bpsk_symbols))))[:num_samps]

    # Convert BPSK symbols to complex (for TX)
    tx_data = data + 1j * np.zeros_like(data)  # BPSK is real-valued

    # Transmit the modulated data
    usrp.send_waveform(tx_data, args.duration, args.freq, args.rate, args.channels, args.gain)

    time.sleep(1)

    # Receive samples
    samps = usrp.recv_num_samps(num_samps, args.freq, args.rate, args.channels, args.gain)

    # BPSK demodulation
    demodulated_bits = bpsk_demodulate(samps)

    # Convert bits back to text
    received_text = bits_to_text(demodulated_bits[:len(bitstring)])  # Trim to the original length
    print("Received Text:", received_text)

    # Save the received samples to file
    with open(args.output_file, 'wb') as out_file:
        if args.numpy:
            np.save(out_file, samps, allow_pickle=False, fix_imports=False)
        else:
            samps.tofile(out_file)

if __name__ == "__main__":
    main()
