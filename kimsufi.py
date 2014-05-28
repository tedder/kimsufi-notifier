#!/usr/bin/python

import requests
from lxml import html,etree
import jinja2
import boto
import os
import sys
from bs4 import BeautifulSoup

data = {}
page = requests.get('http://www.kimsufi.com/ie/', headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'})
#soup = BeautifulSoup(page.text)
#tree = html.fromstring(page.text, "xml")
#tree = BeautifulSoup(page.text, "xml")
tree = etree.fromstring(page.text, etree.HTMLParser())

print page.text.encode("utf-8")
sys.exit()
#print tree

# data['author']
#print tree.xpath("//tr[@data-ref='142sk4']/td[@data-dc='bhs']")
for path in tree.xpath("//td"):
  for ch in path:
    print ch.attrib
    print etree.tostring(ch)

#for tag in soup.find_all(data-ref='142sk4'):
  #print tag

sys.exit()
#print "ch: %s" % tree.xpath("//tr[@data-ref='142sk4']/td[@data-dc='bhs']")[0].getchildren)
for element in tree.xpath("//tr[@data-ref='142sk4']/td[@data-dc='bhs']").getchildren():
  if isinstance(element.tag, basestring):
    print("%s - %s" % (element.tag, element.text))
  else:
    print("SPECIAL: %s - %s" % (element, element.text))
  #print "%s %s" % (k, dir(k))
  #print "%s" % (k.attrib)
  #print "%s" % (k.tag)
#print tree.xpath("//*[@data-ref='142sk1']/td[@data-dc='bhs']/")
#print tree.xpath("//*[@data-ref='142sk1']/td[@data-dc='bhs']/node()")
sys.exit()
data['title'] = ' : '.join([x.strip() for x in tree.xpath("//*[@itemprop='breadcrumb']/li//text()") if x.strip()])

data['items'] = []
for row in tree.xpath("//*[@id='packages_list']/*//tr[contains(@class,'archive_package_row')]"):
  rowstrs = [x.strip() for x in row.xpath("td//text()") if x.strip()]
  if not rowstrs:
    continue
  data['items'].append( (
    rowstrs[0][0],
    URL,
    ' '.join( (rowstrs) )
  ))


# idea stolen from codeape on stackoverflow: http://stackoverflow.com/a/2101186/659298
curr_dir = os.path.dirname(os.path.realpath(__file__))
output_atom = jinja2.Environment(loader=jinja2.FileSystemLoader(curr_dir)).get_template("atomtemplate.xml.j2").render(data)

s3 = boto.connect_s3()
s3key = s3.get_bucket('tedder').new_key('rss/ppa/rquillo.atom')
s3key.set_metadata('Content-Type', 'application/atom+xml')
s3key.set_contents_from_string(output_atom, replace=True, reduced_redundancy=True, headers={'Cache-Control':'public, max-age=3600'}, policy="public-read")

#p = HTMLParser()
#p.feed(packages.text)


