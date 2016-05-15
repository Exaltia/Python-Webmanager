#!/usr/bin/python
# coding=UTF-8
import cgi
import cgitb
import os
from easyzone import easyzone
from Cookie import SimpleCookie
form = cgi.FieldStorage()
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
	tablerecords = nsrecords[i]
	print """<input type="text" id="Autre" name="6" value="%s"><br>""" % (tablerecords)
	i = i +1
#Displaying all MX records
NbrRecords = len(f.root.records('MX').items)
mxrecords = f.root.records('MX').items
i = 0
while (i < NbrRecords):
	print mxrecords
	listrecords = mxrecords[i]
	Nbrlistrecords = len(listrecords)
	print Nbrlistrecords
	print """<input type="text" id="Autre" name="7" value="%s"><input type="text" id="Autre" name="8" value="%s"><br>""" % (listrecords)
	i = i + 1
#Displaying all A records
i = 0
ii = 0
allnames = list(f.names)
zonenamelen = len(allnames)
print zonenamelen
while ( i < zonenamelen):
	currentzonename = allnames[i]
	print "<br>"
	print currentzonename
	#NbrRecordsperNames = len(f.names[currentzonename].records('A').items)
	cnames = f.names[currentzonename].records('CNAME')
	anames = f.names[currentzonename].records('A')
	aaaanames = f.names[currentzonename].records('AAAA')
	txtnames = f.names[currentzonename].records('TXT')
	if cnames:
		strcnames = str(cnames.items)
		strcnames = strcnames.strip("[']")
		print """<input type="text" id="Autre" name="%s" value="%s"><input type="submit" name ="modifcname" value="Modifier"><input type="submit" value="Supprimer">""" % (i, strcnames) 
	elif anames:
		anameslen = len (anames.items)
		if anameslen > 1:
			while ii < anameslen:
				stranames = str(anames.items[ii])
				stranames = stranames.strip("[']")
				separator = ','
				idandvalue = ''
				stri = ''
				stri = str(i)
				idandvalue = stri + separator + stranames
				fqdna = str(currentzonename) + separator + stranames
				print """<input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (stranames, stranames, fqdna)
				print '<br>' + fqdna
				ii = ii + 1
		if anameslen < 2:
			stranames = str(anames.items)
			stranames = stranames.strip("[']")
			fqdna = str(currentzonename) + separator + stranames
			print """<input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (stranames, stranames, fqdna)
			print '<br>' + fqdna
	elif aaaanames:
		ii = 0
		print '<br> ii Value is : '
		print ii
		aaaanameslen = len (aaaanames.items)
		while ii < anameslen:
			straaaanames = str(aaaanames.items)
			straaaanames = straaaanames.strip("[']")
			print """<input type="text" id="Autre" name="Mmmonamemanualinput" value="%s"><input type="submit" value="Modifier">""" % (straaaanames)
			ii = ii +1
	elif txtnames:
		ii = 0
		txtnameslen = len (txtnames.items)
		while ii < anameslen:
			strtxtnames = str(txtnames.items)
			strtxtnames = strtxtnames.strip("[']")
			print """<input type="text" id="Autre" name="Mmmonamemanualinput" value="%s"><input type="submit" value="Modifier">""" % (strtxtnames)
			ii = ii + 1
	else:
		print "Error, the zone has neither a CNAME, A or TXT records"
	# print "Nombre "
	# print NbrRecordsperNames
	#arecords = f.names[currentzonename].records('A').items
	#print type(arecords)
	#print """<input type="text" id="Autre" name="Mmmonamemanualinput" value="%s"><input type="text" id="Autre" name="Mmmonamemanualinput" value="%s"><br>""" % (arecords)
	print i
	i = i + 1
print '<br>'
#if 'grosboutonrouge1'
#print '<form name="formulaire" action="zoneitemchange.py" method="POST">'
print '<input type="submit" name="action" value="Modifier">'
print '<input type="submit" name= "action" value="Supprimer">'
# if "Modifier" in form:
	# print '<form name="formulaire" action="zoneitemchange.py" method="POST">'
# if "Supprimer" in form:
	# print '<form name="formulaire" action="zoneitemdelete.py" method="POST">'
# else:
	# print 'thefuk'
print '<hr>'
print C