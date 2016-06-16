#!/usr/bin/python
import os.path, cgi, os, sys, stat, cgitb, time
from datetime import datetime
import config, pyez_func

if __name__ == '__main__':
    str1 = pyez_func.html_header()
    str1 += '<meta http-equiv="Pragma" content="no-cache">\n'
    str1 += '<meta http-equiv="Cache-Control" content="no-cache">\n'
    str1 += '<meta http-equiv="Expires" content="0">'
    str1 += '</head>\n<body>\n'

    print str1

    # Get file list
    FileList = os.listdir(config.Local_RSI_Dir)
    FileList2 = []
    for f1 in FileList:
        if 'RSI' in f1:
            FileList2.append(os.path.join(config.Local_RSI_Dir, f1))

    FileList2.sort(key=os.path.getmtime, reverse=True)

    str2 = ''
    for item in FileList2:
        filename = os.path.split(item)[1]
        st = os.stat(item)
        str2 += '<tr><td><a href="' + config.HTTP_RSI_Dir  + cgi.escape(filename) + '" target="shita">'
#        print cgi.escape(filename)
        str2 += cgi.escape(filename) + '</td><td>'
        str2 += str(st[stat.ST_SIZE]) + '</td><td>'
        dt = datetime.fromtimestamp(st[stat.ST_MTIME])
        str2 += dt.strftime("%Y-%m-%d %H:%M:%S") + '</td></tr>\r\n'

    str1 = '<b>RSI File(s)</b><br>'
    str1 += '<table border=1>'
    str1 += '<tr><th>Name</th><th>Size</th><th>Date</th></tr>\r\n'
    str1 += str2 + '</table></body></html>'

    print str1

