#!/usr/bin/python

from lxml import html,etree

tree = html.fromstring("""
<table>
 <tr our-row="no">
  <td hello="people"><span>secretA</span></td>
  <td hello="world"><span>secretB</span></td>
 </tr>
 <tr our-row="yes">
  <td hello="people"><span>secret1</span></td>
  <td hello="world">
<span>
secret2
</span>
</td>
 </tr>
</table>
""")

path = tree.xpath("//tr[@our-row='yes']/td[@hello='world']")[0]
print path
print etree.tostring(path)
