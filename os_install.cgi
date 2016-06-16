#!/usr/bin/python
import csv, os, sys, config, pyez_func

if __name__ == '__main__':
    print pyez_func.html_header()
    
# add button
    str4 = '<form method="post" action="test10.cgi" target="shita">\n'
    str4 += '<input type="submit" value="Install the image">'
    print str4

# create target os list
    str3 = '<option value="-" selected>-'
    for filename in os.listdir(config.OS_Dir):
        str3 += '<option value="' + filename + '">' + filename
    str3 += '</select>'

# creat device list table
    str1 = '<table border=1>'
    str1 += '<tr><th>IP Address</th><th>Hostname</th>'
    str1 += '<th>Modle</th><th>Current OS Ver.</th><th>Target OS Ver.</th></tr>\n'

    f_devlists = open(config.Device_List, 'r')
    reader = csv.reader(f_devlists)
    for row in reader:
        str1 += '<tr><td>' + row[0] + '</td>'
        str1 += '<td>' + row[1] + '</td><td>' + row[2] + '</td><td>'
        str1 += row[4] + '</td><td>'
        str1 += '<select name="' + row[0] + '">' + str3 + '</td></tr>\n'
        
    str1 += '</table>'
    print str1

# add candidate os table

    print '</form></body></html>'
