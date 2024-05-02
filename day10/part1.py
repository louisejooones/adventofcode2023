import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# with open('test.txt', 'r') as file:
#   grid = file.read().splitlines()

# Get session cookie from .env
load_dotenv()
session_cookie = os.getenv('SESSION_COOKIE')

# Get input from AdventOfCode website
url = 'https://adventofcode.com/2023/day/10/input'
cookies = {'session': session_cookie}
response = requests.get(url, cookies=cookies)

# Ensure the request was successful
if response.status_code == 200:
  # Split the content by newlines to get a list of lines
  grid = response.text.split('\n')
else:
  print(f'Failed to load page with status code {response.status_code}')

#  Remove the last line, which is empty
grid.pop()

for index, line in enumerate(grid):
  grid[index] = list(line)

print(grid)

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
                   
def get_pipe(x, y):
  return grid[y][x]

def get_direction_from_pipe(pipe, direction):
  if pipe == 'S':
    print("S pipe")
    return "S"
  if direction == "R":
    if pipe == '-':
      return "R"
    elif pipe == 'J':
      return "U"
    elif pipe == '7':
      return "D"
    else:
      return None
  elif direction == "L":
    if pipe == '-':
      return "L"
    elif pipe == 'L':
      return "U"
    elif pipe == 'F':
      return "D"
    else:
      return None
  elif direction == "U":
    if pipe == '|':
      return "U"
    elif pipe == '7':
      return "L"
    elif pipe == 'F':
      return "R"
    else:
      return None
  elif direction == "D":
    if pipe == '|':
      return "D"
    elif pipe == 'L':
      return "R"
    elif pipe == 'J':
      return "L"
    else:
      return None
    
# Find the starting pipe "S" in the grid
for y, row in enumerate(grid):
  for x, pipe in enumerate(row):
    if pipe == 'S':
      start_x = x
      start_y = y

print(f"Start location: {start_x}, {start_y}")

loop_moves = 0
loop_found = False


# Try moving in each direction from the starting pipe
for initial_direction in ['R', 'L', 'U', 'D']:
  print("initial direction:", initial_direction)
  num_of_moves = 0
  x = start_x
  y = start_y
  direction = initial_direction
  while loop_found == False:
    # print(x,y)
    # print(direction)
    x, y = move_direction(direction, x, y)
    # print(x,y)
    pipe = get_pipe(x, y)
    # print(pipe)
    direction = get_direction_from_pipe(pipe, direction)
    # print(direction)
    if direction == None:
      # print("Can't go that way!")
      break
    elif direction == "S":
      # print("Found the start again!")
      # print(f"{pipe} location: {x}, {y}")
      num_of_moves += 1
      loop_moves = num_of_moves
      loop_found = True
      break
    else:
      num_of_moves += 1
      # print(f"Moved to {x}, {y} and found {pipe} so now moving {direction}")

# print(pd.DataFrame(grid))
print(loop_moves/2)
