
import os

LINEAR_REGRESSION = 'linear_reg'
LOGISTIC_REGRESSION = 'log_reg'

def default_model_config():
  mc = ModelConfig('', '', '', '', '', '')
  return mc

class ColsCfg(object):

  def __init__(self, cols_for_learning, cols_for_memorizing):
    self.cols_for_learning = cols_for_learning
    self.cols_for_memorizing = cols_for_memorizing

  def get_cols_for_memorizing(self):
    return self.cols_for_memorizing

  def get_cols_for_learning(self):
    return self.cols_for_learning

class ModelConfig(object):

  def __init__(self, name, learned_model_loc, memorized_model_loc, cols_cfg,
                     feature_map_loc, feature_map2_loc,
                     model_type=LINEAR_REGRESSION):
    """
    Args:
      name: name of the model.
      memorized_model_loc: location of the memorized model.
      cols_cfg: Columns needed to build model.
      feature_map_loc: Location of the feature_map file for feature_selector.FeatureSelector,
        its where where the <feature_name, feature_index> is stored.
      feature_map2_loc: Location of feature_map file for feature_selector.FeatureSelect.
    """
    self.name = name
    self.learned_model_loc = learned_model_loc
    self.memorized_model_loc = memorized_model_loc
    self.feature_map_loc = feature_map_loc
    self.feature_map2_loc = feature_map2_loc
    self.cols_cfg = cols_cfg
    self.model_type=model_type

  def __repr__(self):
    all_attrs = dir(self)
    s = ''
    for attr in all_attrs:
      if attr.startswith('__'):
        continue
      s += '%s: %s ' % (attr, getattr(self, attr))
    return s

class LearnedConfig(object):

  def __init__(self, raw_filenames, model_configs):
    """
    Args:
      raw_filenames: List of raw files passed to the LogsToSeti job.
      model_cfg: A list of ModelConfig objects, one for each model.
    """
    self.raw_filenames = raw_filenames
    self.model_configs = model_configs

  def __repr__(self):
    s = 'filenames: %s\n' % (str(self.raw_filenames))
    for mc in self.model_configs:
      s += 'Model config: %s\n' % (str(mc))
    return s

  def delete_learned_model(self):
    for cfg in self.model_configs:
      cfg.learned_model_loc = ''

def change_dirs(new_dir, model_configs):
  locs = ['learned_model_loc', 'memorized_model_loc', 'feature_map_loc', 'feature_map2_loc']
  for model_config in model_configs:
    for loc in locs:
      base = os.path.basename(getattr(model_config, loc))
      setattr(model_config, loc, os.path.join(new_dir, base))


