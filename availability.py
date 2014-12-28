#!/usr/bin/python

import requests
import sys

try:
  page = requests.get('https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2')
except requests.exceptions.ConnectionError:
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

try:
  sk1 = [x for x in data['answer']['availability'] if x['reference'] == '150sk10'][0]
except TypeError:
  # json failed, which is okay, I think it means no servers are available in any class.
  sys.exit()
bhs = [x for x in sk1['zones'] if x['zone'] == 'bhs'][0]
if bhs['availability'] not in ['unavailable', 'unknown']:
  print bhs['availability']
