import csv

with open('scores.csv') as f:
    reader = csv.reader(f)
    
    c = 0
    for row in reader:
        # print(f'{row[2]}')
        if float(row[2]) > 0.75:
            c += 1
    print(c)

