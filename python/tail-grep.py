#!/usr/bin/python
# -*- coding:utf-8 -*-
# Code by Jioh L. Jung
# Simple Log Tailing and Grep Utility
# - the reason of why I use *nix grep utility(external) is speed.
# - grep/regex on python is more slower than calling of grep utility.

import os
import sys
import pickle
import subprocess

filenm = "/tmp/.log-%s"
filelist = {}
ky = "key"

def save():
  o = open(filenm % ky, "wb")
  pickle.dump(filelist, o)
  o.close()

def load():
  global filelist
  o = open(filenm % ky, "rb")
  filelist = pickle.load(o)
  o.close()

def copyfile(source, dest, pos=0, buffer_size=1024*1024):
  if not hasattr(source, 'read'):
    source = open(source, 'rb')
    source.seek(pos, 0)
  if not hasattr(dest, 'write'):
    dest = open(dest, 'wb')
  while 1:
    copy_buffer = source.read(buffer_size)
    if copy_buffer:
      dest.write(copy_buffer)
    else:
      break
  source.close()
  dest.close()

def dosearch(fname, argv):
  param = []
  param.append(fname)
  param = ["grep"] + argv[1:] + param
  subprocess.call(param)

def main(argv):
  #print argv
  # 1st fname
  fname = argv[0]
  #print fname
  st = None
  try:
    st = os.stat(fname)
  except:
    #print "No such file"
    return
  # Read 1st line as CRC
  fln = ""
  try:
    fln = file(fname, "r").readline()
  except:
    pass
  if not filelist.has_key(fname):
    #print "new!"
    filelist[fname] = {}
    dosearch(fname, argv)
  elif filelist[fname]["size"] > st.st_size:
    #print "sz diff"
    dosearch(fname, argv)
    #elif filelist[fname]["ctime"] != st.st_ctime:
    #print "ctime diff"
    #dosearch(fname, argv)
  elif fln != filelist[fname]["fln"]:
    #print "1st LN diff"
    dosearch(fname, argv)
  elif filelist[fname]["size"] == st.st_size:
    #print "no need search"
    return
  else:
    #print "resume"
    tmpfile = "/tmp/tmpsssss"
    copyfile(fname, tmpfile, pos=filelist[fname]["size"])
    dosearch(tmpfile, argv)
    #os.system("ls -al %s" % tmpfile)
    os.system("rm -f %s" % tmpfile)

  filelist[fname]["size"] = st.st_size  # Size
  filelist[fname]["mtime"] = st.st_mtime # Modification
  filelist[fname]["ctime"] = st.st_ctime # Creation
  filelist[fname]["fln"] = fln
  #print filelist
  save()


if __name__ == "__main__":
  if len(sys.argv) == 1:
    print "%s [key] [target_file] grep_options...." % sys.argv[0]
    exit(1)
  ky = sys.argv[1]
  try:
    load()
  except:
    save()
    #print "ERROR on loading"
  #print filelist
  main(sys.argv[2:])
