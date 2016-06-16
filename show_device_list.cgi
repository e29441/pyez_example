#!/usr/bin/python
import os.path
import csv
import datetime
import config
import pyez_func

def read_facts():
    str1 = ''

    f_devlists = open(config.Device_List, 'w')
    dataWriter = csv.writer(f_devlists)

    ip_lists = pyez_func.get_ip_list()

    for ip_addr in ip_lists:
        filename = config.XML_Dir + ip_addr + '_fact.txt'

        if os.path.isfile(filename):
#                print filename

            f = open(filename, 'r')
            reader = csv.reader(f)

            for row in reader:
                if row[0] != ' ':
                    str1 += '<tr><td><input type="checkbox" name="' + row[0] + '">'
                    str1 += '</td><td><a href=test9.cgi?cmd=show_all&' + row[0] + '=on target="shita">' + row[0] + '</a></td>'
                    str1 += '<td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + row[4] + '</td><td>' + row[3] + '</td></tr>\n'
                        
                    if len(row) == 6:
                        listData = [ row[0], row[1], row[2], row[4], row[3], row[5] ]
                    else:
                        listData = [ row[0], row[1], row[2], row[4], row[3] ]
                    
                    dataWriter.writerow(listData)

    f_devlists.close()
    
    return str1

# main
if __name__ == "__main__":
    str1 = read_facts()

    str2 = '<table border=1>\n<tr><th></th><th>IP Address</th><th>Hostname</th><th>Model</th><th>Serial Number</th><th>OS Version</th></tr>\n' + str1 + '</table>\n'

    str1 = pyez_func.html_header()
    str1 += '<form method="post" action="test9.cgi" target="shita">\n'
    str1 += '<select name="cmd">\n'
    str1 += '<option value="show_mac_table">Show MAC Table</option>\n'
    str1 += '<option value="show_vlan_table">Show VLAN Table</option>\n'
    str1 += '<option value="show_lldp_table">Show LLDP Table</option>\n'
    str1 += '<option value="request_reboot">Reboot Device(s)</option>\n'
    str1 += '<option value="request_halt">Shutdown Device(s)</option>\n'
    str1 += '<option value="get_rsi">Get Request Support Information</option>\n'
    str1 += '</select>\n'
    str1 += '<input type="submit" name="button"><br>\n'
    str1 = str1 + str2 + '</form></body></html>'

    print str1

