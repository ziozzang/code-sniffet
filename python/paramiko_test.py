import paramiko

def run_remote_command(ip, id, pw, cmd, port=22):
  rtn = {}

  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.WarningPolicy())
  client.connect(ip, port, id, pw)
  stdin, stdout, stderr = client.exec_command(cmd)
  
  rtn["stdout"] = []
  
  try:
    for i in p.stdout.read().splitlines():
      # for text processing.
      rtn["stdout"].append(i)
  except AttributeError:
    pass

  #print repr(client.get_transport())
  client.close()

