## vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab
# -*- coding: utf-8 -*-
#
# puprpose: Wake-On-LAN
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import string


def WakeOnLanUDP(ethernet_address, target_iface="eth0", log=None):
  import socket
  import struct
  import os

  # Construct a six-byte hardware address
  addr_byte = ethernet_address.split('-')
  hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
    int(addr_byte[1], 16),
    int(addr_byte[2], 16),
    int(addr_byte[3], 16),
    int(addr_byte[4], 16),
    int(addr_byte[5], 16))

  # Build the Wake-On-LAN "Magic Packet"...
  msg = '\xff' * 6 + hw_addr * 16

  # ...and send it to the broadcast address using UDP
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  if os.uname()[0] == 'Linux':
    # Linux Only
    # -- IN.SO_BINDTODEVICE = 25
    s.setsockopt(socket.SOL_SOCKET, 25, \
      struct.pack(
        "%ds" % (len(target_iface) + 1,),
        target_iface
      )
    )
  else:
    if log is not None:
      log.error("Need Linux System")
    raise NotImplementedError('Need Linux System')

  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  s.sendto(msg, ('<broadcast>', 9))
  s.close()


def WakeOnLanEtherWake(ethernet_address, target_iface="eth0", log=None):
  import subprocess

  # Construct a six-byte hardware address
  addrs = string.join(ethernet_address.split('-'), ':')

  cmd = [ "etherwake", "-i", target_iface, addrs]

  try:
    subprocess.check_call(cmd)

  except e:
    if log is not None:
      log.error("Can't execute 'etherwake': %s" % e)

# Example use
# WakeOnLan('01-13-93-81-68-b2')
