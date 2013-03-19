# -*- coding:utf-8 -*-
# Generate New RSA
# RSA Private key & Public Key for ssh/scp/sftp login
# Original Code URL
#  http://stackoverflow.com/questions/2466401/how-to-generate-ssh-key-pairs-with-python

import os
from Crypto.PublicKey import RSA
import base64


def get_new_rsakey(size=2048):
  # Generate Private Key
  key = RSA.generate(size, os.urandom)
  private_key = key.exportKey()

  # Create public key
  ssh_rsa = '00000007' + base64.b16encode('ssh-rsa')

  # Exponent.
  exponent = '%x' % (key.e, )
  if len(exponent) % 2:
    exponent = '0' + exponent

  ssh_rsa += '%08x' % (len(exponent) / 2, )
  ssh_rsa += exponent

  modulus = '%x' % (key.n, )
  if len(modulus) % 2:
    modulus = '0' + modulus

  if modulus[0] in '89abcdef':
    modulus = '00' + modulus

  ssh_rsa += '%08x' % (len(modulus) / 2, )
  ssh_rsa += modulus

  public_ssh_key = 'ssh-rsa %s' % (
    base64.b64encode(base64.b16decode(ssh_rsa.upper())), )

  public_key = key.publickey().exportKey()

  return private_key, public_key, public_ssh_key


# USAGE
"""
# Sample RSA/SSH Keygen
import rsakeygen

pr, pu, psu = rsakeygen.get_new_rsakey()

print "'%s'" % psu  # SSH Public Key
print pr            # Private Key
print pu            # Public Key

open("ssh-key.ssh-rsa","w").write(psu)
open("ssh-key.key","w").write(pr)
open("ssh-key.pub","w").write(pu)
"""
