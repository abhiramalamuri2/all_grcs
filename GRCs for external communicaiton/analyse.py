from collections import defaultdict

# Dictionary to hold the sequences for each second
sequences_per_second = defaultdict(list)

# File path (replace 'your_file.txt' with the actual file name)
file_path = 'data.txt'

# Open and read the file line by line
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        
        # Extract the timestamp and numbers
        timestamp = parts[0] + " " + parts[1]
        second_timestamp = timestamp[:19]  # Extract up to seconds
        
        numbers = parts[2:]  # Extract the numbers
        sequences_per_second[second_timestamp].extend(numbers)

# Print out the sequences per second
for timestamp, sequence in sequences_per_second.items():
    print(f"{timestamp}: {', '.join(sequence)}")

