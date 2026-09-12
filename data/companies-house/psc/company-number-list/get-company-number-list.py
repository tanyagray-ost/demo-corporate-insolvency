#!/usr/bin/env python3

import csv

numbers = []

with open('../carillion-psc-ownership-with-record-id.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row

    for row in reader:
        for value in row[:2]:  # Get the first two columns
            value = value.strip()  # Remove any leading/trailing whitespace
            if value and value not in numbers:  # Check if the value is not empty
                numbers.append(value)

with open('carillion-psc-company-number-list.txt', 'w') as f:
    for number in numbers:
        f.write(f"{number}\n")  

print(f"Extracted {len(numbers)} unique company numbers and saved to carillion-psc-company-number-list.txt")    

