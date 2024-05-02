import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Get session cookie from .env
load_dotenv()
session_cookie = os.getenv('SESSION_COOKIE')

# Get input from AdventOfCode website
url = 'https://adventofcode.com/2023/day/9/input'
cookies = {'session': session_cookie}
response = requests.get(url, cookies=cookies)

# Ensure the request was successful
if response.status_code == 200:
  # Split the content by newlines to get a list of lines
  lines = response.text.split('\n')
else:
  print(f'Failed to load page with status code {response.status_code}')

# Remove the last line as it is empty
lines.pop()

# Convert each line from a string to a list of numbers
for index, line in enumerate(lines):
  lines[index] = [int(num) for num in line.split(' ')]

final_sum = 0

for line in lines:

  print("starting line")
  all_diffs = {}
  diff_list = line
  i = 0

  # While diff_list is not all_zero
  while not all(diff_list == 0 for diff_list in diff_list):
    print(i)
    print(diff_list)
    # Add the diff_list to the dictionary
    all_diffs[i] = diff_list
    # Find the difference between each consecutive number in the list
    diff_list = [diff_list[i+1] - diff_list[i] for i in range(len(diff_list)-1)]
    # Iterate i
    i += 1

  print("finished line")
  print(all_diffs)
  # Get the key of the last item in the dictionary
  i = max(all_diffs.keys())
  
  while i >= 0:
    value_to_add = all_diffs.get(i + 1, [0])[-1]  # Get value or default to [0]

    all_diffs[i].append(all_diffs[i][-1] + value_to_add)

    i -= 1
  
  final_sum += all_diffs[0][-1]

print(final_sum)