#!/usr/bin/python -u
import datetime, cgi, os, cgitb, sys
from lxml import etree
import read_func
import pyez_func
import config
cgitb.enable()

## main 
if __name__ == "__main__":
    form = cgi.FieldStorage()
    str5 = form.getvalue('cmd','')

    print pyez_func.html_header()
    
#    for x in form.keys():
#        print '%s = %s <br>' % (x, form[x].value)

    ip_lists = pyez_func.get_ip_list()

    for ip_addr in ip_lists:
    
        if form.getvalue(str(ip_addr)) == 'on':
#            print ip_addr + '<br>'
            cmd = form.getvalue('cmd')
            if cmd == 'show_mac_table':
                read_func.read_mac_table(ip_addr, config.XML_Dir + ip_addr + '_mac.xml')
            elif cmd == 'show_vlan_table':
                read_func.read_vlan_table(ip_addr, config.XML_Dir + ip_addr + '_vlan.xml')
            elif cmd == 'show_lldp_table':
                read_func.read_lldp_table(ip_addr, confi.XML_Dir + ip_addr + '_lldp.csv')
            elif cmd == 'request_reboot':
                pyez_func.reboot_device(ip_addr)
            elif cmd == 'get_rsi':
                pyez_func.get_rsi(ip_addr)
            elif cmd == 'send_op_cmds':
                set_cmd = form.getvalue('set_cmds')
                pyez_func.send_op_cmd(ip_addr, set_cmd)
            elif cmd == 'send_commands':
                set_commands = form.getvalue('set_cmds')
                pyez_func.send_set_cmd(ip_addr, set_commands)
            elif cmd == 'show_all':
                read_func.read_vlan_table(ip_addr, config.XML_Dir + ip_addr + '_vlan.xml')
                read_func.read_mac_table(ip_addr, config.XML_Dir + ip_addr + '_mac.xml')
                read_func.read_lldp_table(ip_addr, config.XML_Dir + ip_addr + '_lldp.csv')

    print '</body>\n</html>'
