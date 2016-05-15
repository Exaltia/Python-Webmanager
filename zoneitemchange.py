#!/usr/bin/python
# coding=UTF-8
import cgi
import cgitb
import os
from easyzone import easyzone
from Cookie import SimpleCookie
# import zonecontent This is a a reminder TODO refactoring everything for beter code and use variable import
C = SimpleCookie((os.environ["HTTP_COOKIE"]))
form = cgi.FieldStorage()
var = []
action = []
for item in form.getlist("htmlanames"):
	var.append(item)
print "content-type:text/html"
print C
print
radio = form.getvalue('radiorecordbutton')
fqdna = form.getvalue('radiorecordbutton')
fqdna = fqdna.split(',')
CurrentDomainName = str(C)
CurrentDomainName = CurrentDomainName.split('=')
#print CurrentDomainName
print '<hr>'
print C['Current-domain-name']
for item in form.getlist('action'):
	action.append(item)
print radio
print '<hr>'
action = str(action)
action = action.strip("[']")
print radio
print action
print '<br> fqdn is: '
print fqdna[0]
print '<br>'
fqdn = str(fqdna[0])
arecord = str(fqdna[1])
print fqdn + '<br>'
print arecord + '<br>'
print '<hr>'
if action == 'Modifier':
	# currentrecord = radio
	# newrecord = form.getvalue(radio)
	# print currentrecord 
	# print '<br>' 
	# if type(newrecord) is list:
		# wantedrecord = newrecord[0]
		# print newrecord
		# print wantedrecord
	try:
		zonename = str(CurrentDomainName[1])
		print zonename
		filename = "/var/cache/bind/%s" % zonename
		f = easyzone.zone_from_file(zonename, filename)
		f.names[fqdn].records('A').add(arecord)
		test = f.names[fqdn].records('A').items
	except:
		print 'Foiré!'
elif action == 'Supprimer':
	try:
		zonename = str(CurrentDomainName[1])
		print zonename
		filename = "/var/cache/bind/%s" % zonename
		f = easyzone.zone_from_file(zonename, filename)
		f.names[fqdn].records('A').delete(arecord)
		test = f.names[fqdn].records('A').items
		print '<br>'
		print test
	except:
		print 'Couille dans le potage'
else:
	print 'Error'
# print zonecontent.dnsname This is a a reminder TODO refactoring everything for beter code and use variable import
# print '<br>'
#print C
#print action