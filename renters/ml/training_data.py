
"""
class EasySeti(object):

  def __init__(self, seti):
    self.cols = {}
    for cf in seti.cfs:
      self.d[cf.name] = cf.value

    for bf in seti.bfs:
      self.d[ = pieces[1]

  def feature_value(self, column_name):
"""

class FeatureSelector():

  def __init__(self):
    self.i = 0
    self.feature_to_index = {}

  def build_feature_map(self, setis):
    for seti in setis:
      for bf in seti.bfs:
        if bf in self.feature_to_index:
          # Weve already seen this feature.
          continue
        self.feature_to_index[bf] = self.i
        self.i += 1

  def get_index(self, feature):
    if feature not in self.feature_to_index:
      raise Exception('Unrecognized feature not in SETI data: %s' % (feature))
    return self.feature_to_index[feature]


def canonical_repr(features):
  # Given a list of features, find the canonical representation of it.
  return ''

class TDG(object):

  def __init__(self, fs, cols_cfg):
    """
    Args:
      fs: FeatureSelector object.
      cols_cfg: Configuration which specifies which columns to keep.
    """
    self.fs = fs
    self.cols_cfg = cols_cfg
    self.keep_cols = set(self.cols_cfg)

  def transform(self, setis):
    # Find out which cols are even needed from the SETI (single-col only now)
    # Determine the feature index and generate a signature for that example.
    for seti in setis:
      # For each seti example, find which features to keep to put into the
      # training data feature example.
      features = []
      for bf in seti.bfs:
        pieces = bf.split(':')
        if len(pieces) > 2:
          raise Exception('BF: Col name or value cannot have : in it.')
        col_name, value = pieces[0], pieces[1]
        if col_name not in self.keep_cols:
          continue
        # Keep this binary feature as a feature vector.
        feature_index = self.fs.get_index(bf)
        features.append((feature_index, 1.0))

      # Given the feature vector, come up with its canonical representation.
      seti_model_key = canonical_repr(features)


  def save_memorized_blocks(self, filename, blocks):
    pass