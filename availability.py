#!/usr/bin/python

import requests
import sys

page = requests.get('https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2')
data = page.json()

# silently fail if the data is bad
if not data:
  sys.exit()

sk1 = [x for x in data['answer']['availability'] if x['reference'] == '142sk1'][0]
bhs = [x for x in sk1['zones'] if x['zone'] == 'bhs'][0]
if not bhs['availability'] == 'unavailable':
  print bhs['availability']
