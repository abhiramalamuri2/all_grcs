import numpy as np
from gnuradio import gr
import os
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block - calculates data rate every 5 seconds"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.byte]
        )
        self.example_param = example_param
        self.byte_count = 0
        self.start_time = time.time()

    def work(self, input_items, output_items):
        """Calculate and print the data rate every 5 seconds"""

        # Count the number of bytes received in this work call
        self.byte_count += len(input_items[0])
        
        # Convert the list of bytes to characters
        char_sequence = ''.join([chr(b) for b in input_items[0]])

        # Check the time elapsed since the start of the 5-second interval
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        os.system('echo "{}  Data: {}" > /dev/pts/1'.format(timestamp, char_sequence))
	
        if elapsed_time >= 1:  # Every 5 seconds
            data_rate = self.byte_count / elapsed_time  # Calculate data rate in bytes per second
            os.system('echo "{}, Data Rate: {:.2f} bytes/sec" > /dev/pts/3'.format(timestamp, data_rate))
            
            # Print the data rate with the current timestamp
            
            #os.system('echo "Data Rate:  bytes/sec, Data: {}" > /dev/pts/2'.format(char_sequence))
            
            # Reset the byte count and start time for the next interval
            self.byte_count = 0
            self.start_time = current_time

        output_items[0][:] = input_items[0]  # Pass through the input to the output
        return len(output_items[0])  # Return the length of the output

