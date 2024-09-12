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

    def __init__(self, example_param='Hello'):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param

    def work(self, input_items, output_items):
        #global var
        """Print the signal power in dB to /dev/pts"""
        power_db_0 = 10 * np.log10(np.mean(np.abs(input_items[0])**2))  # Compute power of input 0 in dB
        power_db_1 = 10 * np.log10(np.mean(np.abs(input_items[1])**2))  # Compute power of input 1 in dB
        
        
        #os.system('echo "{:.2f}" > /dev/pts/4'.format(power_db))  # Write to /dev/pts/4
        #power_dp_0=1
        #power_dp_1=0
        #out=input_items[0]
        #out_bytes=input_items.astype(np.byte)
        
        out=0
        
        #Initial Connection
        '''global var
        if power_db_0 > power_db_1:
                var = 'A'
        else:
                var = 'B'
        '''
        
        
        #For subsequent connections
        
        '''
        if power_db_0 - power_db_1 > 5:
        	out = 'Connection Established with A'  # Pass through the input 0 to the output
        	var = 'A'
        elif power_db_1 - power_db_0 > 5:
        	out = 'Connection Established with B'  # Pass through the input 0 to the output	
        	var = 'B'
        
        else:
        	var = f'Connection Retained with {var}'
        	
        	#out = 'Connection Retained with {}'.format(connected_to)
        
       ''' 	
       
        
        #output_items[0][:] = out
        os.system('echo "{}" > /dev/pts/2'.format(self.example_param)) 
        	
        return 1 # Return the length of the output
        
        
        
        
