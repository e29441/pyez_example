from lxml import etree
import sys, csv, os, config

def get_ipaddr(hostname):
    str1 = ''

    f2 = open(config.Device_List, 'r')
    reader2 = csv.reader(f2)

    for row2 in reader2:
        if hostname == row2[1]:
            str1 = '<a href=test9.cgi?cmd=show_all&' + row2[0] + '=on target="shita">' + hostname + '</a>'
            break
    else:
        f2.close()

    return str1

def get_facts(ip_addr, fact):
    str1 = ''
    
    if fact == 'hostname':
        i = 1
    elif fact == 'model':
        i = 2
    elif fact == 'style':
        i = 2

    f2 = open(config.Device_List, 'r')
    reader2 = csv.reader(f2)

    for row2 in reader2:
        if ip_addr == row2[0]:
            str1 = row2[i]
            break
    else:
        f2.close()

#    print 'str1 = ', str1

    if fact == 'style':
        if 'EX46' in str1 or 'EX43' in str1 or 'EX92' in str1:
            str1 = 'VLAN_L2NG'
        elif 'MX' in str1:
            str1 = 'BRDIGE_DOMAIN'
        else:
            str1 = 'VLAN'

    print fact, str1

    return str1

def read_mac_table(ip_addr, filename):
    root = etree.parse(filename)
    str1 = ""
    style = get_facts(ip_addr, 'style')

    if style == 'VLAN':
        mac_entries = root.xpath('//mac-table-entry')
        for entry in mac_entries:
            interface_list = entry.xpath('descendant::mac-interfaces')
            for interface in interface_list:
                mac_addr = entry.find('mac-address').text
                mac_vlan = entry.find('mac-vlan').text
            
                if interface.tag != 'mac-interfaces-list':
                    str1 += '<tr><td>' + mac_addr + '</td><td>' + mac_vlan + '</td><td>' + interface.text + '</td></tr>\n'

    elif style == 'VLAN_L2NG':
        mac_entries = root.xpath('//l2ng-mac-entry')
        for entry in mac_entries:
            mac_addr = entry.find('l2ng-l2-mac-address').text
            mac_vlan = entry.find('l2ng-l2-mac-vlan-name').text
            interface = entry.find('l2ng-l2-mac-logical-interface').text

            str1 += '<tr><td>' + mac_addr + '</td><td>' + mac_vlan + '</td><td>' + interface + '</td></tr>\n'

    hostname = get_facts(ip_addr, 'hostname')
    str2 = '<b>MAC Table of ' + hostname + '(' + ip_addr + ')</b></caption>'
    str2 += '<table border=1><tr><th>MAC Address</th><th>VLAN</th><th>Interfaces</th></tr>'
    str2 += str1 + '</table></br>'

    print str2

def read_vlan_table2(vlans, l2ng):
    str1 = ''

    for vlan in vlans:
        vlan_name = vlan.find(l2ng + 'vlan-name').text
        vlan_id = vlan.find(l2ng + 'vlan-tag').text
        member_ifs = vlan.xpath('descendant::' + l2ng + 'vlan-member-interface')
        if_num = len(member_ifs)
        str1 += '<tr><td rowspan=' + str(if_num) + '>' + vlan_name + '</td>' 
        str1 += '<td rowspan=' + str(if_num) + '>' + vlan_id + '</td>'        

        i = 0
        for member_if in member_ifs:
            if isinstance(member_if.text, str):
                if_text = member_if.text
            else:
                if_text = 'None'

            if i == 0:
                str1 += '<td>' + if_text + '</td></tr>\n'
            else:
                str1 += '<tr><td>' + if_text + '</td></tr>\n'
                    
            i += 1

    return str1

def read_vlan_table(ip_addr, filename):
    print 'def read_vlan_table'
    print ip_addr, filename
    root = etree.parse(filename)
    str1 = ""
    style = get_facts(ip_addr, 'style')

    print ip_addr, style, filename

    if style == 'VLAN':
        # Legacy Switch
        vlan_entries = root.xpath('//vlan')
        str1 = read_vlan_table2(vlan_entries, '')
    elif style == 'VLAN_L2NG':
        # L2NG Switch
        vlan_entries = root.xpath('//l2ng-l2ald-vlan-instance-group')
        str1 = read_vlan_table2(vlan_entries, 'l2ng-l2rtb-')
                
    hostname = get_facts(ip_addr, 'hostname')
    str2 = '<b>VLAN Table of '+ hostname + '(' + ip_addr + ')</b>'
    str2 += '<table border=1><tr><th>VLAN Name</th><th>VLAN ID</th><th>Interfaces</th></tr>' 
    str2 += str1 + '</table></br>'
    print str2

def read_lldp_table(ip_addr, filename):
    if os.path.isfile(filename) == False:
        return

    f = open(filename, 'r')
    reader = csv.reader(f)

    str1 = ""

    for row in reader:
        if row[0] != ' ':
            # search ip_addr of neigbhor device
            hostname = get_ipaddr(row[1])
            if hostname == '':
                hostname = row[1]

            # make table
            str1 += '<tr><td>' + row[0] + '</td><td>'
            str1 += hostname + '</td><td>' + row[2] + '</td></tr>\n'

    hostname = get_facts(ip_addr, 'hostname')
    str2 = '<b>LLDP Table of ' + hostname + '(' + ip_addr + ')</b></caption>'
    str2 += '<table border=1><tr><th>Local Interface</th><th>Remote Hostname</th><th>Remote Interface</th></tr>' 
    str2 += str1 + '</table></br>'
    print str2

    f.close()

if __name__ == "__main__":
    ip_addr = sys.argv[1]
    folder = config.XML_Dir
#    read_lldp_table(ip_addr)
    read_vlan_table(ip_addr, config.XML_Dir + ip_addr + '_vlan.xml')
#    read_mac_table(ip_addr, folder + ip_addr + '_mac.xml')
