def avg(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    
    summ = 0
    for i in range(1, len(lines)):
        summ+=float(lines[i][-6:])
        
    avg = summ/len(lines)
    print(avg)

file_path = 'output.txt'
avg(file_path) 