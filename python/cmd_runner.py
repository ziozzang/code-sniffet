# -*- coding:utf-8 -*-
#
# Running External Command
# This code is use to RUN command via SSH
#
# - code by Jioh L. Jung (ziozzang@gmail.com)
#

import os
import subprocess
import paramiko
import conf
import logging

logging.basicConfig(level=conf.LOG_LEVEL)
log = logging.getLogger(__name__)

def local_exec(shcmd, shell=False):
  p = subprocess.Popen(shcmd, shell=shell, stdout=subprocess.PIPE)
  rtncode = p.wait()
  sout = []
  try:
    for i in p.stdout.read().splitlines():
      # for text processing.
      sout.append(i)
  except AttributeError:
    pass
  return {"code":rtncode, "stdout":sout}

def remote_exec(shcmd, host, port, id, pw=None, shell=False):
  tcmd = None
  if (shell == False) and (type(shcmd) is list):
    for i in shcmd:
      if len(i.split()) > 1:
        i = "\"" + i.replace("\t", "\\t").replace(" " , "\ ").replace("\"", "\\\"") + "\""
      elif (i.find("\"") != -1) or (i.find("&") != -1):
        i = i.replace("\"", "\\\"").replace("&", "\&")
      if tcmd is None:
        tcmd = i
      else:
        tcmd = tcmd + " " + i
    shcmd = tcmd

  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.WarningPolicy())

  err = None

  try:
    if pw == None:
      client.connect(host, port, id)
    else:
      client.connect(host, port, id, pw)
  except Exception, e:
    err = repr(e)
    return {"error": err}

  stdin, stdout, stderr = client.exec_command(shcmd)

  sout = []
  rtncode = 0
  try:
    for i in stdout.read().splitlines():
      sout.append(i)
  except AttributeError:
    pass

  try:
    # Get Return Code
    ei, eo, ee = client.exec_command("echo $?")
    rtncode = int(eo.read().strip())
  except AttributeError:
    pass

  client.close()

  return {"code": rtncode, "stdout":sout}

def remote_file(filename, body, host, port, id, pw=None):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.WarningPolicy())

  err = None

  try:
    if pw == None:
      client.connect(host, port, id)
    else:
      client.connect(host, port, id, pw)
  except Exception, e:
    err = repr(e)
    return {"error": err}

  shcmd = "cat > " + filename + " << EOFEOFEOFEFF\n" + body.replace("$", "\\$")+ "\nEOFEOFEOFEFF"

  stdin, stdout, stderr = client.exec_command(shcmd)

  sout = []
  rtncode = 0
  try:
    for i in stdout.read().splitlines():
      sout.append(i)
  except AttributeError:
    pass

  try:
    # Get Return Code
    ei, eo, ee = client.exec_command("ls " + filename + " 2> /dev/null | wc -l")
    rtncode = int(eo.read().strip())
  except AttributeError:
    pass

  client.close()

  if rtncode > 0:
    return True
  return False

def remote_exist(filename, host, port, id, pw=None):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.WarningPolicy())

  rtncode = 0

  try:
    if pw == None:
      client.connect(host, port, id)
    else:
      client.connect(host, port, id, pw)
  except Exception, e:
    err = repr(e)
    return False

  rtncode = 0
  try:
    # Get Return Code
    ei, eo, ee = client.exec_command("ls " + filename + " 2> /dev/null | wc -l")
    print eo
    rtncode = int(eo.read().strip())
  except AttributeError:
    pass

  client.close()

  if rtncode > 0:
    return True
  return False

def local_file(filename, body):
  open(filename, "wb").write(body)
  return os.path.isfile(filename)

def local_exist(filename):
  return os.path.isfile(filename)

# 리모트(SSH)로 명령을 실행함.
class remote(object):
  def __init__(self, cellid=None):
    self.client = paramiko.SSHClient()
    self.client.load_system_host_keys()
    self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

    if cellid is None:
      cellid = conf.REMOTES_DEFAULT
    if not conf.REMOTES.has_key(cellid):
      cellid = conf.REMOTES_DEFAULT

    try:
      if conf.REMOTES[cellid].has_key("pw"):
        self.client.connect(
            conf.REMOTES[cellid]["host"],
            conf.REMOTES[cellid]["port"],
            conf.REMOTES[cellid]["id"],
            conf.REMOTES[cellid]["pw"]
          )
      else:
        self.client.connect(
            conf.REMOTES[cellid]["host"],
            conf.REMOTES[cellid]["port"],
            conf.REMOTES[cellid]["id"]
          )
    except Exception, e:
      err = repr(e)
      print err

  def __exit__(self):
    self.client.close()

  def shell(self, shcmd, shell=False):
    tcmd = None
    if (shell == False) and (type(shcmd) is list):
      for i in shcmd:
        if len(i.split()) > 1:
          i = "\"" + i.replace("\t", "\\t").replace(" " , "\ ").replace("\"", "\\\"") + "\""
        elif (i.find("\"") != -1) or (i.find("&") != -1):
          i = i.replace("\"", "\\\"").replace("&", "\&")
        if tcmd is None:
          tcmd = i
        else:
          tcmd = tcmd + " " + i
      shcmd = tcmd

    stdin, stdout, stderr = self.client.exec_command(shcmd)

    sout = []
    rtncode = 0
    try:
      for i in stdout.read().splitlines():
        sout.append(i)
    except AttributeError:
      pass

    try:
      # Get Return Code
      ei, eo, ee = self.client.exec_command("echo $?")
      rtncode = int(eo.read().strip())
    except AttributeError:
      pass

    return {"code": rtncode, "stdout":sout}

  def files(self, filename, body):
    shcmd = "cat > " + filename + " << EOFEOFEOFEFF\n" + body.replace("$", "\\$")+ "\nEOFEOFEOFEFF"

    stdin, stdout, stderr = self.client.exec_command(shcmd)

    sout = []
    rtncode = 0
    try:
      for i in stdout.read().splitlines():
        sout.append(i)
    except AttributeError:
      pass

    try:
      # Get Return Code
      ei, eo, ee = self.client.exec_command("ls " + filename + " 2> /dev/null | wc -l")
      rtncode = int(eo.read().strip())
    except AttributeError:
      pass


    if rtncode > 0:
      return True
    return False

  def exist(self, filename):
    rtncode = 0
    try:
      # Get Return Code
      ei, eo, ee = self.client.exec_command("ls " + filename + " 2> /dev/null | wc -l")
      print eo
      rtncode = int(eo.read().strip())
    except AttributeError:
      pass

    if rtncode > 0:
      return True
    return False


import sys
import os
import conf
class RedirectStdStreams(object):
  """
  Stream redrect to foo
  """
  def __init__(self, stdout=None, stderr=None):
    self._stdout = stdout or sys.stdout
    self._stderr = stderr or sys.stderr

  def __enter__(self):
    self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
    self.old_stdout.flush(); self.old_stderr.flush()
    sys.stdout, sys.stderr = self._stdout, self._stderr

  def __exit__(self, exc_type, exc_value, traceback):
    self._stdout.flush(); self._stderr.flush()
    sys.stdout = self.old_stdout
    sys.stderr = self.old_stderr

def runfacade(shcmd,shell=False,conn=None):
  if conf.RUN_LOCAL:
    return runpipe(shcmd, shell=shell)
  else:
    if conf.STDERR_REDIRECT_TO is None:
      dev = open(os.devnull, 'w')
    elif conf.STDERR_REDIRECT_TO == "stdout":
      dev = sys.stdout
    else:
      dev = sys.stderr
    with RedirectStdStreams(stderr=dev):
      return runssh(shcmd, host=conn.host, port=conn.port, id=conn.ip, pw=conn.pw, shell=shell)

