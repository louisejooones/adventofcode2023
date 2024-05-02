import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

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
  # Split the content by newlines to get a list of lines
  lines = response.text.split('\n')
else:
  print(f'Failed to load page with status code {response.status_code}')
# Convert the list of lines to a pandas DataFrame
cal_vals = pd.DataFrame(lines, columns=['cal_val'])

# Add a column which is the first digit added to the last digit in the cal_val column
cal_vals['number'] = cal_vals['cal_val'].apply(lambda x: str(safe_int(find_digit(x, type="first"))) + str(safe_int(find_digit(x, type="last"))))
print(cal_vals)

# Convert the number column to an int and sum it
print(cal_vals['number'].astype(int).sum())