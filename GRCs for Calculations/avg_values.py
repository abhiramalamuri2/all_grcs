import math

def read_first_thirty_lines(file_path):
    values = []
    labels = []
    with open(file_path, 'r') as file:
        for _ in range(30):
            line = file.readline().strip()
            if line:
                value, label = line.split()
                values.append(float(value))
                labels.append(label)
            else:
                break
    
    if len(values) < 30:
        raise ValueError("The file has less than 30 lines")

    average = sum(values) / len(values)
    
    # Calculating the variance
    variance = sum((x - average) ** 2 for x in values) / len(values)
    
    # Calculating the standard deviation
    standard_deviation = math.sqrt(variance)
    
    # Rounding to 4 decimal places
    average = round(average, 4)
    standard_deviation = round(standard_deviation, 4)
    variance = round(variance, 4)
    
    # Determining the majority label
    majority_label = 'A' if labels.count('A') > labels.count('B') else 'B'
    
    values.extend([average, standard_deviation, variance, majority_label])
    
    return values

file_path = 'output.txt'  # replace with your file path

try:
    values = read_first_thirty_lines(file_path)
    print(', '.join(map(str, values)))
except ValueError as e:
    print(e)
except FileNotFoundError:
    print(f"The file {file_path} does not exist")

