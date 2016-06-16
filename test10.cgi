#!/usr/bin/python -u
import datetime, cgi, os, cgitb, sys
from lxml import etree
import read_func
import pyez_func
cgitb.enable()

## main
if __name__ == "__main__":
    form = cgi.FieldStorage()

    print pyez_func.html_header()

    for x in form.keys():
#        print '%s = %s <br>' % (x, form[x].value)
        if form[x].value != '-':
            print '\\\ Try to install OS image(' + form[x].value + ') to ' + x + '<br>'
            pyez_func.install_junos(x, form[x].value)

    print '</body>\n</html>'
