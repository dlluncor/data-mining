
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

import feature_selector

def write_feature_maps_from_seti(model_config, setis):
  fs = feature_selector.FeatureSelector()
  fs.build_feature_map(setis)
  fs.write_feature_map(model_config.feature_map_loc)

  fs2 = feature_selector.FeatureSelect()
  fs2.generate_feature_map(model_config.cols_cfg.get_cols_for_learning(), setis)
  fs2.write_feature_maps(model_config.feature_map2_loc)
  return fs, fs2
