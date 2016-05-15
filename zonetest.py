#!/usr/bin/python
# coding=UTF-8
import cgi
import cgitb
import os
import flask
print "Content-type: text/html"
print
form = cgi.FieldStorage()
print form.getlist("dname")
