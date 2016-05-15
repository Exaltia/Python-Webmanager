#!/usr/bin/python
# coding=UTF-8
import cgi
import cgitb
import os
from easyzone import easyzone
from Cookie import SimpleCookie
from easyzone.zone_check import ZoneCheck
# import zonecontent This is a a reminder TODO refactoring everything for beter code and use variable import
C = SimpleCookie((os.environ["HTTP_COOKIE"]))
form = cgi.FieldStorage()
#form is zonecontent.py
var = [] # Check if this var is still useful
action = []
#check if the following for is still useful, i doubt it
for item in form.getlist("htmlanames"):
	var.append(item)
print "content-type:text/html"
print C #Adding cookie inside http headers
print
#get required info from form in order to process zone changes
radio = form.getvalue('radiorecordbutton')
fqdna = form.getvalue('radiorecordbutton')
fqdna = fqdna.split(',')
CurrentDomainName = str(C)
CurrentDomainName = CurrentDomainName.split('=')
for item in form.getlist('action'):
	action.append(item)
action = str(action)
action = action.strip("[']")
fqdn = str(fqdna[0])
arecord = str(fqdna[1])
if action == 'Modifier': # easyzone doesn't really have a modify function, forcing to do add then delete
	currentrecord = arecord
	newrecord = form.getvalue(arecord) 
	print '<br>' 
	if type(newrecord) is list:
		wantedrecord = newrecord[0]
	else:
		wantedrecord = newrecord
	try:
		zonename = str(CurrentDomainName[1])
		filename = "/var/cache/bind/%s" % zonename
		f = easyzone.zone_from_file(zonename, filename)
		f.names[fqdn].records('A').add(wantedrecord)
		f.names[fqdn].records('A').delete(arecord)
		test = f.names[fqdn].records('A').items
		test = str(test)
		print '<br> test is ' + test
	except:
		print 'Foiré!'
		result = 'NOK' # easyzone check the record validity even before passing it to the isValid function
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
		result = 'NOK'
else:
	print 'Error'
#The destination directory (example : /var/cache/bind) must be owned by www-data:bind
tempfilesuffix = '.tmp'
tempfile = filename + tempfilesuffix
f.save (tempfile, autoserial=True)
dnscheck = ZoneCheck(checkzone='/usr/sbin/named-checkzone')
valid = dnscheck.isValid(zonename, tempfile)
if valid is True and result is not 'NOK': #If we don't check for NOK, easyzone write anyways with
	#	 the old valid info, procing the error message from 
	#the failed f function then the ok one because the old zone is still valid when 
	#rewrited
	print 'ok!'
	f.save (filename, autoserial=True)
	os.remove(tempfile)