import re

# String values evaluated as a true boolean values
TRUE_BOOLEANS = [
  'on', 'true', 'enable', 'enabled', 'yes', 'high', 'ok', '1']
# String values evaluated as a false boolean values
FALSE_BOOLEANS = [
  'off', 'false', 'disable', 'disabled', 'no', 'low', 'ko', '0']


def to_int(value):
  """Parse a string and convert it into a value"""
  if not value:
    return 0
  if isinstance(value, int):
    return value
  if isinstance(value, long):
    return int(value)
  mo = re.match('(?i)^\s*(\d+)\s*(?:([KM])B?)?\s*$', value)
  if mo:
    mult = {'k': (1 << 10), 'm': (1 << 20)}
    value = int(mo.group(1))
    value *= mo.group(2) and mult[mo.group(2).lower()] or 1
    return value
  return int(value.strip(), value.startswith('0x') and 16 or 10)


def to_bool(value, permissive=True):
  if value is None:
    return False
  if isinstance(value, bool):
    return value
  if value.lower() in TRUE_BOOLEANS:
    return True
  if permissive or (value.lower() in FALSE_BOOLEANS):
    return False
  raise AssertionError('"Invalid boolean value: "%s"' % value)


def hexline(data):
  """Convert a binary buffer into a hexadecimal representation"""
  LOGFILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or \
             '.' for x in range(256)])
  src = ''.join(data)
  hexa = ' '.join(["%02x" % ord(x) for x in src])
  printable = src.translate(LOGFILTER)
  return "(%d) %s : %s" % (len(data), hexa, printable)

