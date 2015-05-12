#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

print "Content-Type: text/html"
print
print "Testing"

cgi.test()
