#!/usr/bin/python

import requests
import sys

try:
  page = requests.get('https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2')
except ConnectionError:
  # silently fail if the server fails
  sys.exit()

try:
  data = page.json()
except ValueError:
  # silently fail if the data is bad
  sys.exit()

# silently fail if the data is bad
if not data:
  sys.exit()

sk1 = [x for x in data['answer']['availability'] if x['reference'] == '142sk1'][0]
bhs = [x for x in sk1['zones'] if x['zone'] == 'bhs'][0]
if not bhs['availability'] == 'unavailable':
  print bhs['availability']
