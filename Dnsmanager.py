#!/usr/bin/python
# coding=UTF-8
import cgi
import cgitb
import os
FinalZones = [] 
try:
	f = open('/etc/bind/named.conf.local', 'r')
	#print "content-type:text/html\r\n\r\n"
	#print f
except:
	print "content-type:text/html\r\n\r\n"
	print '<html>'
	print '<head>'
	print '</head>'
	print '<body>'
	print "The dev was too lazy to narrow the error type so... error!"
	print '</body>'
	print '</html>'
for line in f.readlines():
	li=line.strip()
	li=li.strip("{[',")

	if not li.startswith("//"):
		if 'zone' in li:
			li=li.strip('zone ')
			li=li.strip('"')
			FinalZones.append(li)
#print FinalZones
#FinalZones = str(FinalZones)
#print type(FinalZones)
#FinalZones = FinalZones.rstrip("\n")
#print FinalZones
#print config
print "content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '</head>'
print '<body>'
print '<form name="formulaire" action="zonecontent.py" method="POST">'
print '<select name="dname">'
for i in FinalZones:
	print """<option value='%s' name=dname>%s</option>""" % (i, i)
print '</select>'
print '<p><input type="submit" value="Soummettre"></p>'
print '</form>'
print '</body>'
print '</html>'