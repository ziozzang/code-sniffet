# process from /proc
import os

def get_all_process():
  d = {}
  pids= [pid for pid in os.listdir('/proc') if pid.isdigit()]
  for pid in pids:
    print open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()


# process list from psutil
import psutil

# 프로세스 목록을 얻어옴
def get_proc():
  procs = []
  procs_status = {}
  for p in psutil.process_iter():
    try:
      p.dict = p.as_dict(['username', 'get_nice', 'get_memory_info',
                          'get_memory_percent', 'get_cpu_percent',
                          'get_cpu_times', 'name', 'status'])
      try:
        procs_status[str(p.dict['status'])] += 1
      except KeyError:
        procs_status[str(p.dict['status'])] = 1
    except psutil.NoSuchProcess:
      pass
    else:
      procs.append(p)

  # 소팅.
  processes = sorted(procs, key=lambda p: p.dict['cpu_percent'], reverse=True)
  return (processes, procs_status)

