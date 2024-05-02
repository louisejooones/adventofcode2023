import re
import pandas as pd

with open('test.txt', 'r') as file:
    lines = file.read().splitlines()

def count_valid(spring, group):
    if spring == ".":
        return count_valid(spring, group[1:])
    elif spring == "#":
        

for line in lines:
    springs, groups = line.split(' ', 1)
    print(springs)
    print(groups)

    num_valid = 1

    for spring in springs:
        for group in groups:
            if spring == ".":
                pass
            elif spring == "#":

