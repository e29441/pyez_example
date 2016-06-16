#!/usr/bin/python

import config, pyez_func

if __name__ == "__main__":

   f1 = open(config.PyEZ_Dir + 'pyez_func.py', 'r')
   l1 = f1.readlines()
   f1.close()

   print pyez_func.html_header()
   print '<pre><code>'

   for line in l1:
      print line,
   print	

   print '</code></pre></body></html>'
    


