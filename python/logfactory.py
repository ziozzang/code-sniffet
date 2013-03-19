import logging

def logger_factory(logtype='syslog', logfile=None, level='WARNING',
           logid='BlahBlah', format=None):
  # this code has been copied from Trac (MIT modified license)
  logger = logging.getLogger(logid)
  logtype = logtype.lower()
  if logtype == 'file':
    hdlr = logging.FileHandler(logfile)
  elif logtype in ('winlog', 'eventlog', 'nteventlog'):
    # Requires win32 extensions
    hdlr = logging.handlers.NTEventLogHandler(logid,
                          logtype='Application')
  elif logtype in ('syslog', 'unix'):
    hdlr = logging.handlers.SysLogHandler('/dev/log')
  elif logtype in ('stderr'):
    hdlr = logging.StreamHandler(sys.stderr)
  else:
    hdlr = logging.handlers.BufferingHandler(0)

  if not format:
    format = 'BlahBlah[%(module)s] %(levelname)s: %(message)s'
    if logtype in ('file', 'stderr'):
      format = '%(asctime)s ' + format
  datefmt = ''
  if logtype == 'stderr':
    datefmt = '%X'
  level = level.upper()
  if level in ('DEBUG', 'ALL'):
    logger.setLevel(logging.DEBUG)
  elif level == 'INFO':
    logger.setLevel(logging.INFO)
  elif level == 'ERROR':
    logger.setLevel(logging.ERROR)
  elif level == 'CRITICAL':
    logger.setLevel(logging.CRITICAL)
  else:
    logger.setLevel(logging.WARNING)
  formatter = logging.Formatter(format, datefmt)
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr)

  def logerror(record):
    import traceback
    print record.msg
    print record.args
    traceback.print_exc()
  # uncomment the following line to show logger formatting error
  #hdlr.handleError = logerror

  return logger
