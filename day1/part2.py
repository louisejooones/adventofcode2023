import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# It would be more efficient to convert all spelled out numbers to digits first,
# then find the first and last digit. This is because you would only need to perform 
# the conversion operation once for each line, rather than potentially twice if you were 
# to find the first and last digit/spelled out number and then convert them to digits.

def replace_spelled_numbers(string):
  number_mapping = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
  }
  for spelled_number, digit in number_mapping.items():
    string = string.replace(spelled_number, spelled_number+digit+spelled_number)
  return string

# Find the first or last digit in a string
def find_digit(string, type="first"):
  if type == "first":
    match = re.search(r'\d', string)
  elif type == "last":
    match = re.search(r'\d(?=[^\d]*$)', string)
  else:
    raise ValueError("Invalid type. Must be 'first' or 'last'.")

  if match:
    return match.group()
  else:
    return None
  
def safe_int(value):
  return int(value) if value is not None else 0

# Get session cookie from .env
load_dotenv()
session_cookie = os.getenv('SESSION_COOKIE')

# Get input from AdventOfCode website
url = 'https://adventofcode.com/2023/day/1/input'
cookies = {'session': session_cookie}
response = requests.get(url, cookies=cookies)

# Ensure the request was successful
if response.status_code == 200:
  print(response.text)
  # Split the content by newlines to get a list of lines
  lines = response.text.split('\n')
  print(lines)
else:
  print(f'Failed to load page with status code {response.status_code}')
# Convert the list of lines to a pandas DataFrame
cal_vals = pd.DataFrame(lines, columns=['cal_val'])

# Replace the spelled out numbers with digits in the cal_val column
cal_vals['num_cal_val'] = cal_vals['cal_val'].apply(replace_spelled_numbers)

# Add a column which is the first digit added to the last digit in the cal_val column
cal_vals['number'] = cal_vals['num_cal_val'].apply(lambda x: str(safe_int(find_digit(x, type="first"))) + str(safe_int(find_digit(x, type="last"))))
print(cal_vals)

# Convert the number column to an int and sum it
print(cal_vals['number'].astype(int).sum())