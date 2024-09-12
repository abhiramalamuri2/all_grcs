def calculate_transition_ratio(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    if len(lines) < 2:
        # If there are fewer than 2 lines, no transitions can occur
        return 0.0

    transitions = 0

    for i in range(1, len(lines)):
        if lines[i][0:18] != lines[i - 1][0:18]:
            transitions += 1

    transition_ratio = transitions / len(lines)
    return transition_ratio

# Example usage
file_path = 'output.txt'
ratio = calculate_transition_ratio(file_path)
print(f'Transition Ratio: {ratio:.10f}')
