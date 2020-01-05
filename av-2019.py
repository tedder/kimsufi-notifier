#!/usr/bin/env python3

import requests
import json
import hashlib
import datetime
import boto3

FEED_KEY = 'rss/kimsufi.json'
FEED_URL = f'https://dyn.tedder.me/{FEED_KEY}'



def write_json_feed(feedj):
  s3 = boto3.client('s3')
  s3.put_object(
    ACL='public-read',
    Body=json.dumps(feedj),
    Bucket='dyn.tedder.me',
    Key=FEED_KEY,
    ContentType='application/json',
    CacheControl='public, max-age=30' # todo: 3600
  )
  print(f"updated: {FEED_URL}")



ret = requests.get('https://ca.ovh.com/engine/api/dedicated/server/availabilities?country=ca')
retj = ret.json()

feed = {
  'version': 'https://jsonfeed.org/version/1',
  'title': 'kimsufi cheap server status',
  'description': 'watching for cheap skus',
  'home_page_url': 'https://tedder.me/',
  'feed_url': FEED_URL,
  'items': []
}

day_str = datetime.date.today().isoformat()

# 1801sk12	atom d425
for a in retj:
  if not a['hardware'] in ('1801sk12', '1801cask12'): continue
  #print(a)
  for dc in a['datacenters']:
    if dc['availability'] == 'unavailable': continue
    link = f"https://www.kimsufi.com/ca/en/order/kimsufi.xml?reference={a['hardware']}"
    available_str = f"{day_str} {a['hardware']} {a['region']} {dc['datacenter']}"
    bhash = hashlib.blake2b( available_str.encode(), digest_size=16 ).hexdigest()

    #bhash = hashlib.blake2b(data=available_str).hexdigest()
    feed['items'].append({
      'id': bhash,
      'content_html': f'<a href="{link}">{available_str}</a>',
      'url': link,
      'date_published': f'{day_str}T00:00:00.00Z'
    })

write_json_feed(feed)

