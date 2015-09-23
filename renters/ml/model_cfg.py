
LINEAR_REGRESSION = 'linear_reg'
LOGISTIC_REGRESSION = 'log_reg'

def default_model_config():
  mc = ModelConfig('', '', '', '', '', '')
  return mc

class ModelConfig(object):

  def __init__(self, name, learned_model_loc, memorized_model_loc, cols_cfg,
                     feature_map_loc, feature_map2_loc,
                     model_type=LINEAR_REGRESSION):
    """
    Args:
      name: name of the model.
      memorized_model_loc: location of the memorized model.
      cols_cfg: Name of all the columns used in this model.
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

class LearnedConfig(object):

  def __init__(self, raw_filenames, model_configs):
    """
    Args:
      raw_filenames: List of raw files passed to the LogsToSeti job.
      model_cfg: A list of ModelConfig objects, one for each model.
    """
    self.raw_filenames = raw_filenames
    self.model_configs = model_configs