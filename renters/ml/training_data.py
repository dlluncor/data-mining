
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
    pass

class TDG(object):

  def __init__(self, cols_cfg):
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
        feature_index = 0
        features.append((feature_index, 1.0))


  def save_memorized_blocks(self, filename, blocks):
    pass