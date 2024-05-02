import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv



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

with open('test.txt', 'r') as file:
  grid = file.read().splitlines()

for index, line in enumerate(grid):
  grid[index] = list(line)

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

# print(f"Start location: {start_x}, {start_y}")

loop_found = False
loop = {}
directions = []

# Try moving in each direction from the starting pipe
for initial_direction in ['R', 'L', 'U', 'D']:
  # print("initial direction:", initial_direction)
  num_of_moves = 0
  x = start_x
  y = start_y
  direction = initial_direction
  while not loop_found:
    # print(x,y)
    # print(direction)
    x, y = move_direction(direction, x, y)
    # print(x,y)
    pipe = get_pipe(x, y)
    # print(pipe)
    last_direction = direction
    direction = get_direction_from_pipe(pipe, direction)
    # print(direction)
    if direction == None:
      # print("Can't go that way!")
      break
    elif direction == "S":
      # print("Found the start again!")
      # print(f"{pipe} location: {x}, {y}")
      num_of_moves += 1
      loop["direction"] = initial_direction
      loop["num_of_moves"] = num_of_moves
      loop["last_direction"] = last_direction
      loop_found = True
      break
    else:
      num_of_moves += 1
      # print(f"Moved to {x}, {y} and found {pipe} so now moving {direction}")

print(loop)

def convert_s(x, y, initial_direction, last_direction):
  if initial_direction == "R":
    if last_direction == "U":
      return "F"
    elif last_direction == "D":
      return "L"
    elif last_direction == "R":
      return "-"
  elif initial_direction == "L":
    if last_direction == "U":
      return "7"
    elif last_direction == "D":
      return "J"
    elif last_direction == "L":
      return "-"
  elif initial_direction == "U":
    if last_direction == "L":
      return "L"
    elif last_direction == "R":
      return "J"
    elif last_direction == "U":
      return "|"
  elif initial_direction == "D":
    if last_direction == "L":
      return "7"
    elif last_direction == "R":
      return "F"
    elif last_direction == "D":
      return "|"

if loop_found:
  # Convert the starting pipe to the correct pipe
  grid[start_y][start_x] = convert_s(start_x, start_y, loop["direction"], loop["last_direction"])

  # Go back around the loop converting each pipe to an X
  x = start_x
  y = start_y
  direction = loop["direction"]
  while True:
    x, y = move_direction(direction, x, y)
    pipe = get_pipe(x, y)
    grid[y][x] = 'X' + pipe
    direction = get_direction_from_pipe(pipe, direction)
    if direction == None:
      break
  
  print(pd.DataFrame(grid))
  
  # Identify the tiles that are enclosed by the loop of "X"s
  
  # inside = False
  # for y, row in enumerate(grid):
  #   for x, pipe in enumerate(row):
  #     if x < len(row)-1:
  #       if pipe == 'S' or pipe == '7' or pipe == 'J' or pipe == 'F' or pipe == 'L' or pipe == 'I':
  #         continue
  #       elif pipe == '|':
  #         inside = not inside
  #       if inside and grid[y][x+1]:
  #         grid[y][x+1] = 'I'

  num_of_is = 0

  for y, row in enumerate(grid):
    count = 0  # Initialize the count outside the inner loop
    for x, pipe in enumerate(row):
      if pipe == 'X|':  # If the current element is '|', increment the count
        count += 1
      elif pipe in ['X7', 'XL']:
        count += 0.5
      elif pipe in ['XF', 'XJ']:
        count -= 0.5
      elif not pipe.startswith('X') and count % 2 == 1:  # If the count is odd, change the current element to 'I'
        grid[y][x] = 'I'
        num_of_is += 1
      print(x, y, count)  # Print the current indices and the count


print(pd.DataFrame(grid))
print(grid.count('I'))
print(num_of_is)
