"""
  SETI represents a training example to process and to score.
"""

class _CF(object):
  def __init__(self, name, value):
    self.name = name  # E.g., 'property_type'
    self.value = value # E.g., 3.0

  def __repr__(self):
    return "{%s: %s}" % (self.name, self.value)

class SETIExample(object):

  def __init__(self):
    self.cf = []  # all ContinuousFeatures
    self.bf = []  # all BinaryFeatures. They are just strings.

  def add_continuous(self, name, value):
    """
    Args:
      name: "age"
      value: 25
    """
    self.cf.append(_CF(name, value))

  def add_binary(self, column_name, value_str):
    """
    Args:
      column_name: "gender"
      value_str: "m"
    """
    self.bf.append('%s:%s' % (column_name, value_str))

  def __str__(self):
    """Generate a unique string. Sort the CF and sort the BF."""
    return ""

"""
seti.add_binary('property_type', 'COVERTED TO MULTI OCCUPANCY')

'property_type:COVERTED TO MULTI OCCUPANCY'

{
  'property_type:COVERTED TO MULTI OCCUPANCY': 0,
  'property_type:COVERTED TO RESIDENTIAL': 1,
  'property_type:UNFENCED POOL': 2,
}

model = {
  0: 0.3,
  1: 3.0,
  2: -0.2,
}

#score
RenterForm(property_type='UNFENCED_POOL')

seti = SETI(bf=['property_type:UNFENCED_POOL'])
ss = seti_server.load_model(model)
ss.score(seti)

def score(seti):
  binary feature -> feature index.
  lookup feature index weight.
  sum all weights
  compute prediction.
"""
