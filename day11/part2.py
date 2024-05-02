import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv


# # Get session cookie from .env
# load_dotenv()
# session_cookie = os.getenv('SESSION_COOKIE')

# # Get input from AdventOfCode website
# url = 'https://adventofcode.com/2023/day/10/input'
# cookies = {'session': session_cookie}
# response = requests.get(url, cookies=cookies)

# # Ensure the request was successful
# if response.status_code == 200:
#   # Split the content by newlines to get a list of lines
#   grid = response.text.split('\n')
# else:
#   print(f'Failed to load page with status code {response.status_code}')

# #  Remove the last line, which is empty
# grid.pop()

with open('input.txt', 'r') as file:
  grid = file.read().splitlines()

for index, line in enumerate(grid):
  grid[index] = list(line)

print(pd.DataFrame(grid))

def move_direction(direction, x, y):
  if direction == 'U':
    y -= 1
  elif direction == 'D':
    y += 1
  elif direction == 'L':
    x -= 1
  elif direction == 'R':
    x += 1
  return x, y

# Find all the rows that are entirely made of "."
empty_rows = []
for index, row in enumerate(grid):
  if row.count('.') == len(row):
    empty_rows.append(index)

# Find all the columns that are entirely made of "."
empty_columns = []
for index, column in enumerate(zip(*grid)):
  if column.count('.') == len(column):
    empty_columns.append(index)

# Number of galaxies in the grid
print(sum([row.count('#') for row in grid]))

# # Duplicate all the empty rows and columns, working from highest to lowest index
# empty_rows.reverse()
# empty_columns.reverse()

# for index in empty_rows:
#   grid.insert(index, ['.'] * len(grid[0]))

# for index in empty_columns:
#   for row in grid:
#     row.insert(index, '.')

print(pd.DataFrame(grid))

# Give each of the galaxies an ID
for y, row in enumerate(grid):
  for x, column in enumerate(row):
    if column == '#':
      grid[y][x] = f'{x}_{y}'

# Find the difference in x and y between each galaxy
galaxy_differences = []
for y1, row in enumerate(grid):
  for x1, column in enumerate(row):
    if column != '.':
      for y2, row2 in enumerate(grid):
        for x2, column2 in enumerate(row2):
          if column2 != '.' and column != column2:
            distance = abs(x2 - x1) + abs(y2 - y1)
            # Multiply any empty rows or columns between the two galaxies by 1 million
            for index in empty_rows:
              if y1 < index < y2 or y2 < index < y1:
                distance += (1000000-1)
            for index in empty_columns:
              if x1 < index < x2 or x2 < index < x1:
                distance += (1000000-1)
            galaxy_differences.append(distance)

print(sum(galaxy_differences)/2)


