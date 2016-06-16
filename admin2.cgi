#!/usr/bin/python
import cgi, cgitb, os, sys
import config, pyez_func
cgitb.enable()

if __name__ == "__main__":
   form = cgi.FieldStorage()

   print pyez_func.html_header()

   userid = 'userid = "' + form.getvalue('userid') + '"\r\n'
   passwd = 'passwd = "' + form.getvalue('passwd') + '"\r\n'
   start_ip = 'start_ip = "' + form.getvalue('start_ip') + '"\r\n'
   end_ip = 'end_ip = "' + form.getvalue('end_ip') + '"\r\n'

   ip = form.getvalue('start_ip').split('.')
   end_ip2 = form.getvalue('end_ip') + '\r\n'

   f1 = open(config.Param_File, "w")
   f1.write(userid + passwd + start_ip + end_ip)
   f1.close()
   print 'configuration is saved.'

   f2 = open(config.IP_File, 'w')
   ip1 = int(ip[0])
   ip2 = int(ip[1])
   ip3 = int(ip[2])
   ip4 = int(ip[3])
   n = 1
   
   while True: 
      ip_addr = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4) + '\r\n'
      f2.write(ip_addr)
      
      ip4 += 1
      if ip4 == 256:
         ip3 += 1
         ip4 = 0   
         
      if ip3 == 256:
         ip2 += 1
         ip3 = 0

      if ip2 == 256:
         ip1 += 1
         ip2 = 0

      if ip_addr == end_ip2:
#         print 'reach to end<br>'
         break

      # avoid infinit loop
      n += 1
      if n > 100000:
         print 'infinit loop<br>'
         break

   f2.close()

   print '</body>\n</html>\n'
