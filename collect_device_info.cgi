#!/usr/bin/python -u

from pprint import pprint
from jnpr.junos import Device
from jnpr.junos import exception as EzErrors
from jnpr.junos.op.ethport import EthPortTable
from lxml import etree
import threading, sys, time
import jnpr.junos.exception
import pyez_func
import config

def myprint(str1):
    print str1
    sys.stdout.flush()

def get_device_information(t_ip, t_u, t_p):
    myprint(t_ip + " : connecting...<br>")
    dev = Device(host=t_ip, user=t_u, password=t_p)
    try:
        dev.open()
    except Exception as err:
        myprint(t_ip + " : couldn't connect.<br>")
        sys.exit(1)

    filename = config.XML_Dir + t_ip 
    pyez_func.get_basic_info(dev, t_ip, filename + '_fact.txt')

    time.sleep(0.5)

    if 'EX' in dev.facts['model']:
        pyez_func.get_vlan_info(dev, t_ip, filename + '_vlan.xml')
        pyez_func.get_mac_table(dev, t_ip, filename + '_mac.xml')
        pyez_func.get_ether_int(dev, t_ip, filename + '_int.xml')
        pyez_func.get_lldp_info(dev, t_ip, filename + '_lldp.csv')

    myprint(t_ip + " : Complete.<br>")

    dev.timeout = 60
    dev.close()
        
# main
if __name__ == "__main__":
    pyez_func.initial_work()

    print pyez_func.html_header()

    userid, passwd, start_ip, end_ip = pyez_func.read_param()

    ip_lists = pyez_func.get_ip_list()
    if len(ip_lists) == 0:
        print 'no ip address serach\r\n'
    else:

        for ip_addr in ip_lists:
            if ip_addr != '':
                
                th_me = threading.Thread(target=get_device_information, name="th_me", args=(ip_addr, userid, passwd,))
                th_me.start()

    print "</body></html>"




