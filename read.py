import csv

with open("Audit.csv",'r') as file:
    csvreader = csv.reader(file)

    for row in csvreader:
        print(row)