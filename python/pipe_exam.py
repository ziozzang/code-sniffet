import subprocess
import re

def _get_ip(iface):
  execinfo = ['ifconfig',
               iface
             ]
  proc = subprocess.check_output(execinfo)

  rval = []
  rexp = re.compile("inet addr:([\d\.]+)\s+Bcast:([\d\.]+)\s+Mask:([\d\.]+)")
  for line in proc.split('\n'):
    matched = rexp.match(line.strip())
    if type(matched) != type(None):
      grps = matched.groups()
      return grps[0]

  return ""
