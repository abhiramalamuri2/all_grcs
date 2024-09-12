"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import os


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.byte, np.byte, np.byte],
            out_sig=[np.byte]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param

    def work(self, input_items, output_items):
        """Print the signal power in dB to /dev/pts"""
        #os.system('echo "{:.2f}" > /dev/pts/4'.format(power_db))  # Write to /dev/pts/4
        if  input_items[2]==0:
        	output_items[0][:] = input_items[0]  # Pass through ofdm signal 0 to the output
        else:
        	output_items[0][:] = input_items[1]  # Pass through ofdm signal 1 to the output
        	
        return len(output_items[0])  # Return the length of the output
