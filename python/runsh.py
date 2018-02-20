# only 2.x versions
import sys

if sys.version_info.major == 2:
  import commands
elif sys.version_info.major == 3:
  import subprocess

# 단일 명령을 실행.
def runsh(shell):
  if sys.version_info.major == 2:
    res = commands.getstatusoutput(shell)
  elif sys.version_info.major == 3:
    res = subprocess.getstatusoutput(shell)
  return (res[0], (shell,res[1])) # ret_code, stdout

# stop 플래그를 켜면 중간에 중단함
def runshlines(shell, stop=True):
  lst = []
  cmd = ""
  for i in shell.splitlines():
    i = i.strip()
    if len(i) == 0 or i[0] == "#":
      continue
    if i[-1] == "\\":
      cmd += i
      continue
    else:
      cmd += i
    res = runsh(cmd)
    lst.append(res[1])
    cmd = "" # Reset
    if stop and res[0] != 0:
      return (res[0], lst)
  return (0, lst)

exit(0)
###########
# Get Current DIR's file list
runsh("ls")[1][1].splitlines()

# Get Docker images UUID
[x.split()[2] for x in runsh("sudo docker images")[1][1].splitlines()][1:]
