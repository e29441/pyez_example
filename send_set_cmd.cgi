#!/usr/bin/python
import os.path, cgi, cgitb, csv, datetime, pyez_func, config
cgitb.enable()

def read_facts(ip_addr):
    filename = config.XML_Dir + ip_addr + '_fact.txt'
    if os.path.isfile(filename) == False:
        return

    f = open(filename, 'r')
    reader = csv.reader(f)

    for row in reader:
        if row[0] != ' ':
            str1 = '<tr><td><input type="checkbox" name="' + row[0] + '"></td><td>' + row[0]
            str1 += '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + row[4] + '</td><td>' + row[3] + '</td></tr>\n'
            return str1

# main
if __name__ == "__main__":
    form = cgi.FieldStorage()

    ip_lists = pyez_func.get_ip_list()
    str1 = ""

    for ip_addr in ip_lists:
        result =  str(read_facts(ip_addr))
        if result != "None":
            str1 += result

    table_c = '<table border=1>\n<tr><th></th><th>IP Address</th><th>Hostname</th><th>Model</th><th>Serial Number</th><th>OS Version</th></tr>\n' + str1 + '</table>\n'

    # header
    s_header = pyez_func.html_header()
    s_header += '<form method="post" action="test9.cgi" target="shita">\n'

    # input box
    if form.getvalue('cmd') == 'op':
        str3 = 'show version\n'
        str3 += 'show chassis hardware\n'
    else:
        d = datetime.datetime.today()
        str3 = 'set system login message "==== Set by PyEZ ' + d.strftime('%Y-%m-%d %H:%M:%S') + ' ===="\n'
        str3 += 'set snmp description "==== Set by PyEZ ' + d.strftime('%H:%M:%S') + '  ===="'
    s_header += '<textarea name="set_cmds" cols=100 rows=5>' + str3 + '</textarea><br>'

    # button
    if form.getvalue('cmd') == 'op':
        s_header += '<input type="hidden" name="cmd" value="send_op_cmds">\n'
    else:
        s_header += '<input type="hidden" name="cmd" value="send_commands">\n'
    s_header += '<input type="submit" name="button"><br><br>\n'

    # table
    contents = s_header + table_c + '</form></body></html>'

    print contents
