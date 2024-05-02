import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# # Get session cookie from .env
# load_dotenv()
# session_cookie = os.getenv('SESSION_COOKIE')

# # Get input from AdventOfCode website
# url = 'https://adventofcode.com/2023/day/8/input'
# cookies = {'session': session_cookie}
# response = requests.get(url, cookies=cookies)

# # Ensure the request was successful
# if response.status_code == 200:
#   # Split the content by newlines to get a list of lines
#   lines = response.text.split('\n')
# else:
#   print(f'Failed to load page with status code {response.status_code}')

with open('test.txt', 'r') as file:
  lines = file.read().splitlines()

instructions = lines.pop(0)

lines.pop(0)

# Make a dictionary to store the values of each register
nodes = {}
for line in lines:
  # The key is the text before the first space
  key = line.split(' ')[0]
  # Create a  list of values: the two three-letter words, with all symbols and whitespace stripped
  values = line.split(' ')[1:]
  values = [word for value in values for word in re.findall(r'[a-zA-Z]{3}', value)]

  nodes[key] = values

print(instructions)

current_node_key = 'AAA'
index = 0
counter = 0

print(nodes[current_node_key])
print(nodes['ZZZ'])

while current_node_key != 'ZZZ':
  current_node = nodes[current_node_key]
  # print(index)
  # print(current_node_key)

  # If instructions[index] does not exist, start again from 0
  if index >= len(instructions):
    index = 0
  elif instructions[index] == 'L':
    current_node_key = current_node[0]
    counter += 1
    index += 1
  else:
    current_node_key = current_node[1]
    counter += 1
    index += 1

print(counter)
