#!/usr/bin/python
import os.path
import csv
import datetime, shutil, sys, commands
import pyez_func

if __name__ == "__main__":

    userid, passwd, start_ip, end_ip = pyez_func.read_param()
    
    str1 = pyez_func.html_header()
    str1 += 'Administration'
    str1 += '<form method="post" action="admin2.cgi" target="ue">\n'
    str1 += '<table>'
    str1 += '<tr><th>start ip address<td><input type="text" name="start_ip" value="' + start_ip + '">'
    str1 += '<tr><th>end ip address <td><input type="text" name="end_ip"  value="' + end_ip + '">'
    str1 += '<tr><th>device username <td><input type="text" name="userid" value="' + userid + '">'
    str1 += '<tr><th>device password <td><input type="text" name="passwd" value="' + passwd + '">'
    str1 += '<tr><th><td><input type="submit" value="Configure">'
    str1 += '</table></form></html>'

    print str1



