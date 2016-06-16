from jnpr.junos import Device
from jnpr.junos import exception as EzErrors
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.config import Config
from jnpr.junos.utils.fs import FS
from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.scp import SCP
from jnpr.junos.exception import *
from lxml import etree
import os, stat, datetime, shutil, sys, commands
import config

def myprint(str1):
    print str1
    sys.stdout.flush()

def html_header():
    str1 = 'Content-type:text/html; charset=utf-8\n\n'
    str1 += '<html>\n<body>\n'
    return str1

def read_param():
    f1 = open(config.Param_File,"r")
    lines = f1.readlines()
    f1.close()

    userid, passwd, ip1, ip2 = [], [], [], []
    for line in lines:
        if line.startswith("userid") is True:
            userid = line.split('"')
        if line.startswith("passwd") is True:
            passwd = line.split('"')
        if line.startswith("start_ip") is True:
            start_ip = line.split('"')
        if line.startswith("end_ip") is True:
            end_ip = line.split('"')

    return (userid[1], passwd[1], start_ip[1], end_ip[1])

def call_dev(ip_addr):
    userid, passwd, start_ip, end_ip = read_param()
    dev = Device(host=ip_addr, user=userid, password=passwd)
    return dev

def get_ip_list():
    f1 = open(config.IP_File, 'r')
    ip_list = f1.read()
    f1.close()

    ip_lists = ip_list.split('\r\n')

    return ip_lists

def get_basic_info(dev, ip_addr, filename):
    myprint(ip_addr + " : getting basic information...<br>")
    #print(ip_addr + " : getting basic information...<br>")
    print dev.facts
    
    hostname = dev.facts['hostname']
    model = dev.facts['model']
    if model == 'Virtual Chassis':
        print 'This is VC'
#        print dev.facts['master']
        Master = dev.facts['master']
#        print dev.facts[Master]['model']
        model = dev.facts[Master]['model'] + '_VC'
    print model

    osver = dev.facts['version']
    serialnum = dev.facts['serialnumber']
    if 'EX46' in model or 'EX43' in model or 'EX92' in model:
        style = 'VLAN_L2NG'
    elif 'MX' in model:
        style = 'BRIDGE_DOMAIN'
    else:
        style = 'VLAN'
    print style
    str1 = ip_addr + ',' + hostname + ',' + model + ',' + osver + ','
    str1 += serialnum + ',' + style + '\n'
    f = open(filename, 'w')
    f.write(str1)
    f.close()

def get_vlan_info(dev, ip_addr, filename):
    print ip_addr, ' : ', filename
    result = dev.rpc.get_vlan_information()

    f = open(filename, 'w')
    f.write(etree.tostring(result))
    f.close()

def get_ether_int(dev, ip_addr, filename):
    try:
        result = dev.rpc.get_ethernet_switching_interface_information()
    except Exception as err:
        return

    f = open(filename, 'w')
    f.write(etree.tostring(result))
    f.close()

def get_mac_table(dev, ip_addr, filename):
    try:
        result = dev.rpc.get_ethernet_switching_table_information()
    except Exception as err:
        if os.path.isfile(filename):
            os.remove(filename)
            return

    f = open(filename, 'w')        
    f.write(etree.tostring(result))
    f.close()

def get_lldp_info(dev, ip_addr, filename):
#    print ip_addr, ' : Getting LLDP Info<br>'
    try:
        result = dev.rpc.get_lldp_neighbors_information()
    except Exception as err:
        return

    f = open(filename, 'w')
    switch_style =  dev.facts['switch_style']
    
    for x in result.findall('.//lldp-neighbor-information'):
        if switch_style == 'VLAN_L2NG':
            local_port = x.find('lldp-local-port-id').text
        elif switch_style == 'VLAN':        
            local_port = x.find('lldp-local-interface').text
            
        remote_chassis_id = x.find('lldp-remote-chassis-id').text
        remote_port = x.find('lldp-remote-port-description').text
        remote_sysname = x.find('lldp-remote-system-name').text
        str1 = local_port + ',' + remote_sysname + ',' + remote_port + '\r\n'
#        print str1
        f.write(str1)

    f.close()
#    print etree.tostring(result)
    return

def send_set_cmd(ip_addr, set_commands):
    myprint(ip_addr + " : connecting...<br>")
    dev = call_dev(ip_addr)
    dev.open(gather_facts=False)

    cu = Config(dev)

    str1 = set_commands.replace('\n', '<br>')
    myprint(ip_addr + " : sending commmand(s) <br>" + str1 + "<br>")
    cu.load(set_commands, format="set")

    myprint("<br>" + ip_addr + " : Committing...<br>")
    cu.commit(timeout=int(60))
    dev.close()

    myprint(ip_addr + " : Completed<br>")

def reboot_device(ip_addr):
    dev = call_dev(ip_addr)

    try:
        dev.open(gather_facts=False)
    except Exception as err:
        return
    else:
        sw = SW(dev)
        rsp = sw.reboot()
        dev.close()

def get_rsi(ip_addr):
    dev = call_dev(ip_addr)

    myprint(ip_addr + ' : accessing... <br>')
    try:
        dev.open(gather_facts=False)
    except Exception as err:
        return

    myprint(ip_addr + ' : creating RSI file...<br>')
    ts = datetime.datetime.today().strftime('%Y%m%d%H%M')
    RSI_File = 'RSI_' + ts + '.txt'
    RSI_File2 = config.Temp_Dir + RSI_File
    myprint(RSI_File + '<br>')
    myprint(RSI_File2 + '<br>')
    opcmd = 'op url ' + config.RSI_Slax + ' rsi-file "' + RSI_File2 + '"'
    myprint(opcmd + '<br>')
    dev.timeout = 120
    sw = dev.cli(opcmd, warning=False)

    myprint(ip_addr + ' : uploading RSI file to this server...<br>')
    RSI_File3 = ip_addr + '_' + RSI_File
    cu = FS(dev)
    cu.cp(RSI_File2, config.FileSrv + RSI_File3)

#    print ip_addr, " : Finished<br>"
    str1 = ip_addr + ' : Complete creating RSI file. Click <a href="' + config.HTTP_RSI_Dir + RSI_File3 + '">here</a> to download.<br>'
    myprint(str1)

    dev.close()

def install_junos(ip_addr, image_file):
    # calucurate MD5
    md5 = commands.getoutput('md5sum -b %s' % cofig.OS_Dir + '/' + image_file).split()
    local_md5 = md5[0]
    print 'local md5 =  ', local_md5, '<br>'

    dev = call_dev(ip_addr)

    try:
        dev.open(gather_facts=False)
        dev.timeout = 1800
        
        # copy the image
        print 'Copying os image. please wait...<br>'
        junos_image_file = config.Temp_Dir + image_file
        cu = FS(dev)
        result = cu.cp(config.OSImage_Dir + image_file, junos_image_file)

        # calcurate MD5 on device
        remote_md5 = cu.checksum(junos_image_file)

        print 'remote md5 = ', remote_md5, '<br>'

        if local_md5 == remote_md5:
            print 'Complete file copy successfully.<br>'

            # install the image
            print 'Start junos update. please wait...<br>'
            sw = SW(dev)
            result = sw.pkgadd(junos_image_file)
            
            if result is True:
                print 'OS installation process finished successfully.<br>'
            else:
                print 'OS installation process finished with failure.<br>'
        else:
            print 'Complete file copy with failure.<br>'

    except Exception as err:
        print err
    else:
        dev.close()

def send_op_cmd(ip_addr, op_cmd):
    dev = call_dev(ip_addr)

    myprint('===== Device IP : ' + ip_addr + ' =====<br>')

    try:
        dev.open(gaterh_facts=False)
    except Exception as err:
        return

    cmds = op_cmd.splitlines()
    for cmd in cmds:
        myprint('----- the output of "' + cmd + '" -----')

        dev.timeout = 300
        sw = dev.cli(cmd, warning=False)
        print '<pre><code>' + sw + '</code></pre>'
        myprint('')

    dev.close()

def try_function(ip_addr):
    dev = call_dev(ip_addr)
    dev.open()
  
    get_basic_info(dev, ip_addr, config.XML_Dir + ip_addr)
    get_vlan_info(dev, ip_addr, config.XML_Dir + ip_addr + '_vlan.xml')

    dev.close()

if __name__ == '__main__':
    print sys.argv[1]
    ip_addr = sys.argv[1]
#    call_dev(ip_addr)
    try_function(ip_addr)
#    install_junos(ip_addr)
#    send_op_cmd(ip_addr, 'show version')
#    send_op_cmd(ip_addr, 'show security dynamic-address ')

  
