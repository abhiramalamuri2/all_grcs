import random
no_of_chars = 1000

def string_to_bits(input_string):
    # Convert string to a bit sequence using ASCII encoding
    return ''.join(format(ord(char), '08b') for char in input_string)

def calculate_bit_error_rate(ref_bits, file_bits):
    # Calculate the bit error rate (BER) between two bit sequences
    if len(ref_bits) != len(file_bits):
        raise ValueError("Bit sequences must be of the same length")

    num_errors = sum(1 for x, y in zip(ref_bits, file_bits) if x != y)
    bit_error_rate = num_errors / len(ref_bits)
    return bit_error_rate

# Define a reference string
reference_contents = "2KxRfYzpb8ppxuAAreTj1MQX9mRALqT8UUA2FZJxfS4FKvDNYdK2AKkYfKfGg20xdcD1vv4gq1GP6v4we7MYUeDi6q1JCzL667Gw\n"
reference_string = reference_contents*1000

# Convert reference string to bit sequence
reference_bits = string_to_bits(reference_string)[:70000]

# Read the contents of a file (change the file path as needed)
file_path = '/home/aerolifi/Documents/GRCs/out.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the first 1000 characters of the file
    file_content = file.read(1000 * len(reference_contents))

# Convert file content to bit sequence
file_bits = string_to_bits(file_content)[:70000]

# Calculate bit error rate between reference bits and file bits
bit_error_rate = calculate_bit_error_rate(reference_bits, file_bits)

# Print the calculated bit error rate
print(f"Bit Error Rate: {bit_error_rate:.6f}")


#this file complies the ber between the reference and the data received
#for some reason the ber of the data received is very high when we use the random characters from file2.txt
#but with file1 where there's only hello world, it gives a 0 ber. look into this
