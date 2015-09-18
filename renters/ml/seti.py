"""
  SETI represents a training example to process and to score.
"""

class _CF(object):
  def __init__(self, name, value):
    self.name = name  # E.g., 'property_type'
    self.value = value # E.g., 3.0


class SETIExample(object):

  def __init__(self):
    self.cf = []  # all ContinuousFeatures
    self.bf = []  # all BinaryFeatures. They are just strings.

  def add_continuous(self, name, value):
    self.cf.append(_CF(name, value))

  def add_binary(self, column_name, value_str):
    self.bf.append('%s:%s' % (column_name, value_str))

  def __str__(self):
    """Generate a unique string. Sort the CF and sort the BF."""
    return ""