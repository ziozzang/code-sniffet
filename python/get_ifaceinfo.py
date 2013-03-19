import socket
import struct

def iptoint(ipstr):
  return struct.unpack('!I', socket.inet_aton(ipstr))[0]

def inttoip(ipval):
  return socket.inet_ntoa(struct.pack('!I', ipval))

#같은 서브넷이면 NIC 정보를 돌려줌.
def get_iface_config(address):
  if not address:
    return None
  try:
    import netifaces
  except ImportError:
    raise AssertionError("netifaces module is not installed")
  pool = iptoint(address)
  for iface in netifaces.interfaces():
    ifinfo = netifaces.ifaddresses(iface)
    if netifaces.AF_INET not in ifinfo:
      continue
    for inetinfo in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
      addr = iptoint(inetinfo['addr'])
      mask = iptoint(inetinfo['netmask'])
      ip = addr & mask
      ip_client = pool & mask
      delta = ip ^ ip_client
      if not delta:
        config = {'ifname': iface,
              'server': inttoip(addr),
              'net': inttoip(ip),
              'mask': inttoip(mask)}
        return config
  return None

