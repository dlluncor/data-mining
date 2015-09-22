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
  """Create feature vector creates a feature vector from a SETI input.
  
    This method will probably be deprecated because this was our first understanding
    of what a feature vector looked like.
  """
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

def to_readable_vector(fs, setie):
  """Creates a list of (feature_key, feature_val) for the feature vector in readable form.

  Args:
    fs: FeatureSelect object.
    setie: the SetiInput we mean to transform to a list of tuples of readable keys.
  """
  all_cols_set = set(fs.all_col_names)
  
  v = {}
  for col_name in fs.all_col_names:
    v[col_name] = 0.0

  ds = DigestedSETI(setie)
  for col, val_to_info in fs.bf_col_map.iteritems():
    bf_val = ds.get_bf_value(col)
    col_key = col + '_' + 'MISSING'
    if bf_val is not None:
      col_key = col + '_' + bf_val
      if col_key not in all_cols_set:
        # Dont create an entry for an element which does not exist in the model.
        continue
    v[col_key] = 1.0
  for col, _ in fs.cf_col_map.iteritems():
    cf_val = ds.get_cf_value(col)
    if cf_val is not None:
      v[col] = cf_val
  return v

def float_feature_vector(fs, setie):
  """Creates a list of floats for the feature vector.

  Args:
    fs: FeatureSelect object.
    setie: the SetiInput we mean to transform to a list of floats.
  """
  v = []
  ds = DigestedSETI(setie)
  for col, val_to_info in fs.bf_col_map.iteritems():
    # Does this column exist in the SETI?
    bf_val = ds.get_bf_value(col)
    # By default whether a feature is true or not for a categorical feature is
    # false unless we see it to be true.
    vals_for_col = [0 for _ in xrange(len(val_to_info)-1)]
    if bf_val is None:
      # Set the MISSING bit to true.
      vals_for_col[0] = 1
    else:
      index_of_feature = val_to_info.keys().index(bf_val)
      if index_of_feature != 1:
        # Only set any bits to true when the implicit value at position 1 is not
        # set.
        vals_for_col[index_of_feature-1] = 1
    # Add the values to the feature vector.
    v.extend(vals_for_col)

  for col, _ in fs.cf_col_map.iteritems():
    cf_val = ds.get_cf_value(col)
    if cf_val is None:
      v.append(0)
    else:
      v.append(cf_val)
  return v

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

class DigestedSETI(object):

  def __init__(self, seti):
    self._reset(seti)

  def _reset(self, setie):
    self.bf_map = {}
    for bf in setie.bfs:
      parts = bf.split(':')
      col, val = parts[0], parts[1]
      self.bf_map[col] = val
    self.cf_map = {}
    for cf in setie.cfs:
      self.cf_map[cf.name] = cf.value

  def get_cf_value(self, col):
    if col not in self.cf_map:
      return None
    return self.cf_map[col]

  def get_bf_value(self, col):
    if col not in self.bf_map:
      return None
    return self.bf_map[col]



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
