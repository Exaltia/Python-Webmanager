#!/usr/bin/python
# coding=UTF-8
#Version 0.0.1Alpha
#In order to handle IPV6 AAAA records correctly, you MUST edit file 
#/usr/local/lib/python2.7/dist-packages/easyzone-1.2.2-py2.7.egg/easyzone/easyzone.py
#and add the following code after line 337:
#	elif rectype == 'AAAA':
#        name = args[0]
#        rd = dns.rdtypes.IN.AAAA.AAAA(dns.rdataclass.IN, dns.rdatatype.AAAA, name)
# or switch to vimalloc forked version of easyzone
#https://github.com/vimalloc/easyzone
#Otherwize, zoneitemchange.py will return an error when adding the record
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
stranames = ''
strcnames = ''
straaaanames = ''
strtxtnames = ''
#Loop for form crafting
try:
	while ( i < zonenamelen):
		currentzonename = allnames[i]
		print "<br>"
		print currentzonename
		cnames = f.names[currentzonename].records('CNAME')
		anames = f.names[currentzonename].records('A')
		aaaanames = f.names[currentzonename].records('AAAA')
		txtnames = f.names[currentzonename].records('TXT')
		if cnames:
			ii = 0
			cnameslen = len(cnames.items)
			while ii < cnameslen:
				strcnames = str(cnames.items)
				strcnames = strcnames.strip("[']")
				fqdnc = 'CNAME' + separator + str(currentzonename) + separator + strcnames
				print '<hr>' + fqdnc + '<hr>'
				print """IN CNAME <input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (strcnames, strcnames, fqdnc) 
				ii = ii + 1
		elif anames:
			anameslen = len (anames.items)
			print anameslen
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
					print """IN A <input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (stranames, stranames, fqdna)
					ii = ii + 1
			if anameslen < 2:
				stranames = str(anames.items)
				stranames = stranames.strip("[']")
				fqdna = 'A' + separator + str(currentzonename) + separator + stranames
				print """IN A <input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (stranames, stranames, fqdna)
		elif aaaanames:
			ii = 0
			aaaanameslen = len (aaaanames.items)
			while ii < aaaanameslen:
				straaaanames = str(aaaanames.items)
				straaaanames = straaaanames.strip("[']")
				fqdnaaaa = 'AAAA' + separator + str(currentzonename) + separator + straaaanames # Staying alive ! :)
				print """IN AAAA <input type="text" id="Autre" name="%s" value="%s"><input type="radio" name="radiorecordbutton" value="%s">""" % (straaaanames, straaaanames, fqdnaaaa)
				ii = ii +1
		elif txtnames:
			ii = 0
			txtnameslen = len (txtnames.items)
			while ii < txtnameslen:
				strtxtnames = str(txtnames.items)
				strtxtnames = strtxtnames.strip("""["']""")
				fqdntxt = 'TXT' + separator + str(currentzonename) + separator + strtxtnames
				print """IN TXT <input type="text" id="Autre" name="%s" value=%s><input type="radio" name="radiorecordbutton" value=%s>""" % (strtxtnames, strtxtnames, fqdntxt)
				ii = ii + 1
		# else:
			# print 'the problematic record is: ' + stranames + strcnames + straaaanames + strtxtnames
			# print "The zone has neither a CNAME, A or TXT records, is it still to be considered as an error?"
		i = i + 1
except:
	print 'General error, contact admin if it occurs again'
print '<br>'
print '<input type="submit" name="action" value="Modifier">'
print '<input type="submit" name= "action" value="Supprimer">'