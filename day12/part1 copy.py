import re
import pandas as pd

with open('test.txt', 'r') as file:
    lines = file.read().splitlines()

input = pd.DataFrame()

input[['grid', 'groups']] = pd.DataFrame(line.split(' ', 1) for line in lines)

input['groups'] = input['groups'].str.split(',').tolist()
input['grid'] = "." + input['grid'] + "."

# Find the largest group in groups
input['largest_group'] = input['groups'].apply(lambda x: max(x))

# Steps:
# Create the regex pattern for the largest group
input['regex'] = input['largest_group'].apply(int).apply(lambda x: x * "#")

# Find the starting index of the largest group in the grid
input['starting_index'] = input.apply(
    lambda row: row['grid'].find(row['regex']), axis=1
)

# Find the ending index of the largest group in the grid
input['ending_index'] = input.apply(
    lambda row: row['starting_index'] + len(row['regex'])
    if row['starting_index'] >= 0
    else 1000, axis=1
)

# If the starting index is >=0, then replace the element on the left of regex with a .
input['grid'] = input.apply(
    lambda row: row['grid'][:row['starting_index']] +
    "." + row['grid'][row['starting_index']:]
    if row['starting_index'] >= 0
    else row['grid'], axis=1
)

# If the ending index is less than the length of the grid, then replace the element on the right of regex with a .
input['grid'] = input.apply(
    lambda row: row['grid'][:row['ending_index']] +
    "." + row['grid'][row['ending_index']+1:]
    if row['ending_index'] < len(row['grid'])
    else row['grid'], axis=1
)


print(input)
