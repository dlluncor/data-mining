
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

import csv, seti

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

      for cf in seti.cfs:
        if cf in self.feature_to_index:
          # Weve already seen this feature.
          continue
        self.feature_to_index[cf.name] = self.i
        self.i += 1

  def get_index(self, feature):
    if feature not in self.feature_to_index:
      raise Exception('Unrecognized feature not in SETI data: %s' % (feature))
    return self.feature_to_index[feature]


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
    price_blocks = []
    for seti_input in setis:
      # For each seti example, find which features to keep to put into the
      # training data feature example.
      features = seti.create_feature_vector(self.fs, self.keep_cols, seti_input)

      # Given the feature vector, come up with its standard representation.
      seti_model_key = seti.standard_repr(features)
      price_blocks.append((seti_model_key, seti_input.label))

    return price_blocks

  def save_memorized_blocks(self, filename, blocks):
    with open(filename, 'wb') as fin:
      writer = csv.writer(fin)
      for block in blocks:
        print(block)
        writer.writerow(block)
