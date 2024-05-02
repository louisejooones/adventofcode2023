import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Function to find the maximum number of a colour in a string
def find_max_colour(text, colour):
  numbers = []
  for match in re.finditer(colour, text):
    start_index = max(0, match.start() - 3)
    substring = text[start_index:match.start()].strip()
    if substring.isdigit():
      numbers.append(int(substring))
  return max(numbers, default=0) if numbers else 0

# Get session cookie from .env
load_dotenv()
session_cookie = os.getenv('SESSION_COOKIE')

# Get input from AdventOfCode website
url = 'https://adventofcode.com/2023/day/2/input'
cookies = {'session': session_cookie}
response = requests.get(url, cookies=cookies)

# Ensure the request was successful
if response.status_code == 200:
  # Split the content by newlines to get a list of lines
  lines = response.text.split('\n')
  # Remove the last line as it is empty
  lines.pop()
else:
  print(f'Failed to load page with status code {response.status_code}')

# Convert the list of lines to a pandas DataFrame
games = pd.DataFrame(lines, columns=['text'])

# Find the game number
games['num'] = games['text'].apply(lambda x: int(re.search(r'Game (\d+):', x).group(1)))

# Find the maximum number of cubes of each colour
for colour in {"blue", "red", "green"}:
  games[colour] = games['text'].apply(lambda x: find_max_colour(x, colour))

print(games)

# Find the power of the minimum number of cubes
games["power"] = games.apply(lambda x: x["blue"] * x["red"] * x["green"], axis=1)

# Sum the game minimum power column
print(games["power"].sum())