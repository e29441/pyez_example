#!/usr/bin/python
import os.path, cgi, os, sys, stat
import cgitb, time
from datetime import datetime
import config, pyez_func

if __name__ == "__main__":
    str1 = pyez_func.html_header()
    str1 += '<meta http-equiv="Pragma" content="no-cache">\n'
    str1 += '<meta http-equiv="Cache-Control" content="no-cache">\n'
    str1 += '<meta http-equiv="Expires" content="0">'
    str1 += '</head>\n<body>\n'
    str1 += '<b>Upload OS Image</b><br>'
    str1 += '<form method="post" enctype="multipart/form-data" action="show_osimage.cgi" target="shita">\n'
    str1 += '<input type="file" name="file1"><br>'
    str1 += '<input type="submit" value="UPLOAD">'
    str1 += '</form>'

    str2 = '<b>OS Image(s)</b><br>'
    str2 += '<table border=1>'
    str2 += '<tr><th>Name</th><th>Size</th><th>Date</th></tr>'
    
    for fname in sorted(os.listdir(config.OS_Dir)):
#        fname = normalize(fname)
        pname = os.path.join(config.OS_Dir, fname)
        st = os.stat(pname)
        str2 += '<tr><td>' + cgi.escape(fname) + '</td><td>'
        str2 += str(st[stat.ST_SIZE]) + '</td><td>'
        dt = datetime.fromtimestamp(st[stat.ST_MTIME])
        str2 += dt.strftime("%Y-%m-%d %H:%M:%S") + '</td></tr>'

    str2 += '</table>'

    print str1 + str2 + '</body></html>'
