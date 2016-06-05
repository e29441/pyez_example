IP_Address = 'localhost'

PyEZ_Dir = '/var/www/pyez/'
XML_Dir = PyEZ_Dir + 'xmls/'
Param_File = PyEZ_Dir + 'credentials.txt'
IP_File = PyEZ_Dir + 'ip_list.txt'
Device_List = PyEZ_Dir + 'device_list.txt'

# OS Image
OS_Dir = PyEZ_Dir + 'junos'
OSImage_Dir = 'http://' + IP_Address + '/pyez/junos/'

# RSI File
Temp_Dir = '/var/tmp/'
Local_RSI_Dir = '/home/lab/public_html'
RSI_Slax = 'http://' + IP_Address + '/pyez/get_rsi.slax'
HTTP_RSI_Dir = 'http://' + IP_Address + '/~lab/'
FileSrv = 'ftp://lab:Juniper@' + IP_Address + '/public_html/'
