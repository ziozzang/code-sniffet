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

