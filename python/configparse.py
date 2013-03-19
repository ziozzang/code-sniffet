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

