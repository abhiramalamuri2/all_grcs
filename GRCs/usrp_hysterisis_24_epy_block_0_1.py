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
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param

    def work(self, input_items, output_items):
        """Print the signal power in dB to /dev/pts"""
        #power_db_0 = 10 * np.log10(np.mean(np.abs(input_items[0])**2))  # Compute power of input 0 in dB
        #power_db_1 = 10 * np.log10(np.mean(np.abs(input_items[1])**2))  # Compute power of input 1 in dB
        
        
        #os.system('echo "Power A: {:.2f}" > /dev/pts/1'.format(power_db_0))  # Write to /dev/pts/4
        #os.system('echo "Power B: {:.2f}" > /dev/pts/2'.format(power_db_1))
        #power_dp_0=1
        #power_dp_1=0
        #out=input_items[0]
        #out_bytes=input_items.astype(np.byte)
        
        out= 'A'
        
        '''
        if power_db_0 - power_db_1 > 5:
        	out = 'Connection Established with A'  # Pass through the input 0 to the output
        	connected_to = 'A'
        elif power_db_1 - power_db_0 > 5:
        	out = 'Connection Established with B'  # Pass through the input 0 to the output	
        	connected_to = 'B'
        
        else:
        	out = 'Connection Retained'
        	#out = 'Connection Retained with {}'.format(connected_to)
        	
        '''
        
        '''
        if power_db_0 > power_db_1:
        	out = 'Connected to A \t\t Power A: {:.2f}  \t\t Power B: {:.2f}'.format(power_db_0, power_db_1)  # Pass through the input 0 to the output
        else:
        	out = 'Connected to B \t\t Power A: {:.2f}  \t\t Power B: {:.2f}'.format(power_db_0, power_db_1)
       '''
        
        
        #Hard Decision Handover
        '''
        if power_db_0 > power_db_1:
                out = '{:.2f} A'.format(power_db_0)  # Pass through the input 0 to the output
        else:
                out = '{:.2f} B'.format(power_db_1) 
        
        '''
        '''
        ratio = power_db_1/power_db_0
        if ratio < 1/1.5:
                out = 'B\t\t\t {:.2f}'.format(power_db_1)  # Pass through the input 0 to the output
        else:
                out = 'A\t\t\t {:.2f}'.format(power_db_0)
        '''
                
         
        #No Handover algorithm      
        '''
        if power_db_0 > power_db_1:
                out = '{:.2f} B'.format(power_db_1)  # Pass through the input 0 to the output
        else:
                out = '{:.2f} B'.format(power_db_1) 
        
        '''
        	
       
        
        #output_items[0][:] = out
        os.system('echo "{}" > /dev/pts/1'.format(out)) 
        	
        return len(output_items[0])  # Return the length of the output
        
        
        
        
