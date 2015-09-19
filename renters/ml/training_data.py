
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

class TDGBlock(object):

  def __init__(self, feature_vector, label):
    self.feature_vector = feature_vector
    self.label = label


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
    #print(setis)
    tdg_blocks = []
    for seti_input in setis:
      # For each seti example, find which features to keep to put into the
      # training data feature example.
      features = seti.create_feature_vector(self.fs, self.keep_cols, seti_input)
      # Given the feature vector, come up with its standard representation.
      tdg_blocks.append(TDGBlock(features, seti_input.label))
    return tdg_blocks
