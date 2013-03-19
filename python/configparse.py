from ConfigParser import SafeConfigParser

#ini style config parser
class EasyConfigParser(SafeConfigParser):
  "ConfigParser extension to support default config values"
  def get(self, section, option, default=None):
    if not self.has_section(section):
      return default
    if not self.has_option(section, option):
      return default
    return SafeConfigParser.get(self, section, option)

# simple config reader(as ini format)
def _get_conf(fname):
  conf = {}
  for l in open(fname, "r").readlines():
    l = l.strip()
    if len(l) == 0 or l[0] == '#':
      continue
    p = l.split('=', 1)
    if len(p) == 2:
      k = p[0].strip()
      v = p[1].strip()
      conf[k] = v

  return conf
