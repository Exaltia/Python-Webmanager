#!/usr/bin/python
# coding=UTF-8
import cgi
import cgitb
import os
from easyzone import easyzone
from Cookie import SimpleCookie
form = cgi.FieldStorage()
#form is Dnsmanager.py
dnsname = form.getlist("dname")
dnsname = str(dnsname)
dnsname = dnsname.strip("[']")
zoneNS = [] 
C = SimpleCookie()
C["Current-domain-name"] = dnsname # Explicit variable name PLEASE!!!111oneoneone
try:
	#Standard notation of open doesn't work for easyzone.zone_from_file
	zonename = "%s" % dnsname
	filename = "/var/cache/bind/%s" % dnsname
	f = easyzone.zone_from_file(zonename, filename)
except :
	#Todo : Make a real error message and a real error handling
	print "content-type:text/html"
	print
	print '<html>'
	print '<head>'
	print '</head>'
	print '<body>'
	print "The dev was too lazy to narrow the error type so... error!"
	print "prout<br>"
	print dnsname + "test"
	print "file name is "
	print '</body>'
	print '</html>'
#f is the file opened by zone_from_file... yeah yeah i know, very explicit variable name
namelist = list(f.names)
print "content-type:text/html"
print C
print
print '<form name="formulaire" action="zoneitemchange.py" method="POST">'
print """<H3>Domaine en cours: %s</H3>"""  % f.domain
print '<br><br>'
print """<input type="text" id="Autre" name="1" value="%s"><br>""" % (f.root.soa.serial)
print """<input type="text" id="Autre" name="2" value="%s"><br>""" % (f.root.soa.refresh)
print """<input type="text" id="Autre" name="3" value="%s"><br>""" % (f.root.soa.retry)
print """<input type="text" id="Autre" name="4" value="%s"><br>""" % (f.root.soa.expire)
print """<input type="text" id="Autre" name="5" value="%s"><br>""" % (f.root.soa.minttl)
#Displaying all NS records
NbrRecords = len(f.root.records('NS').items)
nsrecords = f.root.records('NS').items
tablerecords = ''
i = 0
while (i < NbrRecords):
	tablerecords = nsrecords[i] #Add the required code to allow modification
	print """<input type="text" id="Autre" name="6" value="%s"><br>""" % (tablerecords)
	i = i +1
#Displaying all MX records
NbrRecords = len(f.root.records('MX').items)
mxrecords = f.root.records('MX').items
i = 0
while (i < NbrRecords):
	listrecords = mxrecords[i]
	Nbrlistrecords = len(listrecords)
	#Add the required code to allow modification
	print """<input type="text" id="Autre" name="7" value="%s"><input type="text" id="Autre" name="8" value="%s"><br>""" % (listrecords)
	i = i + 1
#Displaying all A records
i = 0
ii = 0
allnames = list(f.names)
zonenamelen = len(allnames)
separator = ','
#Loop for form crafting
while ( i < zonenamelen):
	currentzonename = allnames[i]
	print "<br>"
	print currentzonename
	cnames = f.names[currentzonename].records('CNAME')
	anames = f.names[currentzonename].records('A')
	aaaanames = f.names[currentzonename].records('AAAA')
	txtnames = f.names[currentzonename].records('TXT')
	if cnames:
		strcnames = str(cnames.items)
		strcnames = strcnames.strip("[']")
		fqdnc = 'C' + separator + str(currentzonename) + separator + strcnames
		print """<input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (strcnames, strcnames, fqdnc) 
	elif anames:
		anameslen = len (anames.items)
		if anameslen > 1:
			#handle if there is more than 1 A record for a single fqdn
			while ii < anameslen:
				stranames = str(anames.items[ii])
				stranames = stranames.strip("[']")
				idandvalue = ''
				stri = ''
				stri = str(i)
				idandvalue = stri + separator + stranames
				fqdna = 'A' + separator + str(currentzonename) + separator + stranames
				print """<input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (stranames, stranames, fqdna)
				ii = ii + 1
		if anameslen < 2:
			stranames = str(anames.items)
			stranames = stranames.strip("[']")
			fqdna = 'A' + separator + str(currentzonename) + separator + stranames
			fqdna = str(currentzonename) + separator + stranames
			print """<input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (stranames, stranames, fqdna)
	elif aaaanames:
		ii = 0
		aaaanameslen = len (aaaanames.items)
		while ii < anameslen:
			straaaanames = str(aaaanames.items)
			straaaanames = straaaanames.strip("[']")
			fqdnaaaa = 'AAAA' + separator + str(currentzonename) + separator + straaaanames # Staying alive ! :)
			print """<input type="text" id="Autre" name="Mmmonamemanualinput" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (straaaanames, fqdna)
			ii = ii +1
	elif txtnames:
		ii = 0
		txtnameslen = len (txtnames.items)
		while ii < anameslen:
			strtxtnames = str(txtnames.items)
			strtxtnames = strtxtnames.strip("[']")
			fqdntxt = 'TXT' + separator + str(currentzonename) + separator + strtxtnames
			print """<input type="text" id="Autre" name="Mmmonamemanualinput" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (strtxtnames, fqdna)
			ii = ii + 1
	else:
		print "Error, the zone has neither a CNAME, A or TXT records"
	i = i + 1
print '<br>'
print '<input type="submit" name="action" value="Modifier">'
print '<input type="submit" name= "action" value="Supprimer">'