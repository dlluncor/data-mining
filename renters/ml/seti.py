"""
  SETI represents a training example to process and to score.
"""

def standard_repr(features):
  """
  Given a list of features, find the standard representation of it.
  features: a list of feature, (idx, val). Below inputs should have same output
    [(0, 5.0), (10, 0.2), (4, 0.4)]
    [(10, 0.2), (0, 5.0), (4, 0.4)]
  return: string presentation of the feature, like:
    '0-5.0:4-0.4:10-0.2'
  """
  if features is None:
      return ''

  sorted_features = sorted(features, key=lambda x: x[0])

  return ':'.join('%s-%s' % (idx, val) for idx, val in sorted_features)

def create_feature_vector(fs, keep_cols, seti):
  features = []
  for bf in seti.bfs:
    pieces = bf.split(':')
    if len(pieces) > 2:
      raise Exception('BF: Col name or value cannot have : in it.')
    col_name, value = pieces[0], pieces[1]
    if col_name not in keep_cols:
      continue
    # Keep this binary feature as a feature vector.
    feature_index = fs.get_index(bf)
    features.append((feature_index, 1.0))

  for cf in seti.cfs:
    if cf.name not in keep_cols:
      continue
    feature_index = fs.get_index(cf.name)
    features.append((feature_index, cf.value))
  return features

def create_seti(label, bfs=None, cfs=None, weight=1.0):
  s = SETIExample()
  if bfs is not None:
    for bf in bfs:
      s.add_binary(bf[0], bf[1])
  if cfs is not None:
    for cf in cfs:
      s.add_continuous(cf[0], cf[1])
  s.weight = weight
  s.label = label
  return s

class _CF(object):

  def __init__(self, name, value):
    self.name = name  # E.g., 'property_type'
    self.value = value # E.g., 3.0

  def __repr__(self):
    return "{%s: %s}" % (self.name, self.value)

class SETIExample(object):

  def __init__(self):
    self.cfs = []  # all ContinuousFeatures
    self.bfs = []  # all BinaryFeatures. They are just strings.
    self.weight = 1
    self.label = -1

  def add_continuous(self, name, value):
    """
    Args:
      name: "age"
      value: 25
    """
    self.cfs.append(_CF(name, value))

  def add_binary(self, column_name, value_str):
    """
    Args:
      column_name: "gender"
      value_str: "m"
    """
    self.bfs.append('%s:%s' % (column_name, value_str))

  def __repr__(self):
    """Generate a unique string. Sort the CF and sort the BF."""
    s = ""
    s += str(self.bfs)
    s += str(self.cfs)
    s += 'Weight: %.2f. Label: %.2f' % (self.weight, self.label)
    return s

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
