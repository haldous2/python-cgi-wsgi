#!/usr/bin/env python
import cgi
import cgitb

form = cgi.FieldStorage()
operands = form.getlist('operand')
total = 0
for operand in operands:
    try:
        value = int(operand)
    except ValueError:
        value = 0
    total += value

output = str(total)

print "Content-Type: text/html"
#print "Content-Length: %s" % len(output)
print
print "the sum is %s" % output
print "<form method='post'>"
print "<input name='operand' />"
print "<input name='operand' />"
print "<input name='operand' />"
print "<input name='operand' />"
print "<input name='operand' />"
print "<input type='submit' name='submit' />"
print "</form>"
