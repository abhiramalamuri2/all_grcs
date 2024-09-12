import random
no_of_chars = 1000

def string_to_bits(input_string):
    # Convert string to a bit sequence using ASCII encoding
    return ''.join(format(ord(char), '08b') for char in input_string)


    num_errors = sum(1 for x, y in zip(ref_bits, file_bits) if x != y)
    bit_error_rate = num_errors / len(ref_bits)
    return bit_error_rate

# Define a reference string
reference_string = "Hello, world!\n"*1000

# Convert reference string to bit sequence
reference_bits = string_to_bits(reference_string)

# Read the contents of a file (change the file path as needed)
file_path = '/home/aerolifi/Documents/GRCs/out.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the first 1000 characters of the file
    file_content = file.read(1000*14)

print(file_content)

#this file just prints the contents of the output file. 
#try different things on the gnuradio grc and see how the output differs.