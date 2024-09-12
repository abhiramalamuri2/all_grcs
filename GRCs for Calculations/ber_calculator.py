def calculate_error_rate(file_path):
    total_lines = 0
    error_count = 0

    # Open the file for reading
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            total_lines += 1
            # Remove leading/trailing whitespace and compare to 'Hello World'
            if line.strip() != 'Hello World':
                error_count += 1

    # Calculate error rate
    error_rate = error_count / total_lines if total_lines > 0 else 0.0

    return error_rate

# Example usage:
file_path = 'output.txt'  # Replace with your file path
error_rate = calculate_error_rate(file_path)
print(f"Error rate: {error_rate:.2%}")
