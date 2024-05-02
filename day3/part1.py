# import re
# import requests
# import pandas as pd
# import os
# from dotenv import load_dotenv



# # Get session cookie from .env
# load_dotenv()
# session_cookie = os.getenv('SESSION_COOKIE')

# # Get input from AdventOfCode website
# url = 'https://adventofcode.com/2023/day/3/input'
# cookies = {'session': session_cookie}
# response = requests.get(url, cookies=cookies)

# # Ensure the request was successful
# if response.status_code == 200:
#   # Split the content by newlines to get a list of lines
#   lines = response.text.split('\n')
#   # Remove the last line as it is empty
#   lines.pop()
# else:
#   print(f'Failed to load page with status code {response.status_code}')

# spare_row = "." * len(lines[0])
# lines.insert(0, spare_row)
# lines.append(spare_row)

# spare_column = "."
# for index, line in enumerate(lines):
#   lines[index] = spare_column + line + spare_column

# # print(lines)

# # Create a dictionary of indices for each line
# all_number_indices = {}

# for index, line in enumerate(lines):
#   # Go along the line and find any numbers
#   numbers = re.findall(r'\d+', line)

#   number_indices = {}

#   for number in numbers:
#     # Convert the number to an integer
#     number_int = int(number)

#     # Find the start index of the number in the line
#     start_index = line.find(number)

#     # Add all indices between start_index and end_index to a list
#     all_indices = list(range(start_index, start_index + len(number)))

#     # Add the number to the dictionary
#     number_indices[number_int] = all_indices
    
#   all_number_indices[index] = number_indices


# all_symbol_indices = {}

# for index, line in enumerate(lines):
#   # Make a list of the indices of all the symbols except "." and numerical digits on this line 
#   symbols_except_dot_indices = [i for i, char in enumerate(line) if char != '.' and not char.isdigit()]

#   all_symbol_indices[index] = symbols_except_dot_indices


# def find_neighbours(index, line_number):
#   neighbours = []
  
#   # Check the previous line
#   if line_number > 0:
#     neighbours.append([line_number - 1, index])
#     if index > 0:
#       neighbours.append([line_number - 1, index - 1])
#     if index < len(lines[line_number - 1]) - 1:
#       neighbours.append([line_number - 1, index + 1])
  
#   # Check the current line
#   if index > 0:
#     neighbours.append([line_number, index - 1])
#   if index < len(lines[line_number]) - 1:
#     neighbours.append([line_number, index + 1])
  
#   # Check the next line
#   if line_number < len(lines) - 1:
#     neighbours.append([line_number + 1, index])
#     if index > 0:
#       neighbours.append([line_number + 1, index - 1])
#     if index < len(lines[line_number + 1]) - 1:
#       neighbours.append([line_number + 1, index + 1])
  
#   return neighbours

# sum = 0

# for row, numbers in all_number_indices.items():
#   for number, indices in numbers.items():

#     # Initialize a flag variable
#     symbol_neighbour_found = False

#     for index in indices:
#       # Find the indices of all the nearest neighbours of this number
#       neighbours = find_neighbours(index, row)

#       # print(neighbours)

#       # Check if any of the neighbours are symbols
#       for neighbour in neighbours:
#         # print(neighbour)
#         if neighbour[1] in all_symbol_indices[neighbour[0]]:
#           # Set the flag variable to True
#           symbol_neighbour_found = True

#     # If a symbol neighbour was found, break out of the loop
#     if symbol_neighbour_found:
#       # Add the number to the sum
#       sum += number

# print(sum)

import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

with open('input.txt', 'r') as file:
  lines = file.read().splitlines()

symbols = set()
for line in lines:
  symbols.update(set(line))
symbols.discard('.')
symbols.discard('\n')
# discard numbers
for i in range(10):
  symbols.discard(str(i))

# Add a spare row and column of "." to surround the grid
spare_row = "." * len(lines[0])
lines.insert(0, spare_row)
lines.append(spare_row)

spare_column = "."
for index, line in enumerate(lines):
  lines[index] = spare_column + line + spare_column

# print(lines)

# Create a dictionary of indices for each line
number_indices = {}

for index, line in enumerate(lines):
  # Go along the line and find any numbers
  numbers = [num for num in re.split(r'\D', line) if num]

  for number in numbers:
    # Convert the number to an integer
    number_int = int(number)

    for match in re.finditer(r'\b' + number + r'\b', line):
      start_index = match.start()
      end_index = match.end()

      # Add all indices between start_index and end_index to a list
      all_indices = list(range(start_index, end_index))

      # Add the number to the dictionary
      number_indices[str(index) + "_" + str(start_index) + "_" + str(number)] = {"row": index, "start_index": int(start_index), "end_index": int(end_index), "value": number_int}


# print(number_indices)

def is_symbol(row, index):
  if lines[row][index] in symbols:
    return True
  else:
    return False

sum_total = 0

for key in number_indices:
  found_symbol_neighbour = False
  number = number_indices[key]


  neighbour_indices = list(range(int(number["start_index"]) - 1, int(number["end_index"]) + 1))
  print("neighbour indices are " + str(neighbour_indices))

  rows = [number["row"] - 1, number["row"], number["row"] + 1]
  print("rows are " + str(rows))

  for row in rows:
    for index in neighbour_indices:
      if 0 <= row < len(lines) and 0 <= index < len(lines[row]):
        if 0<= index < len(lines[row]) and is_symbol(row, index):
          found_symbol_neighbour = True
  
  if found_symbol_neighbour:
    sum_total += number["value"]
    print(str(number["row"]) + " contains " + str(number["value"]))

print(sum_total)

# all_sum = 0

# # sum all the numbers in lines
# for line in lines:
#   numbers = re.findall(r'\d+', line)
#   for number in numbers:
#     all_sum += int(number)

# print(all_sum)