
class ModelConfig(object):

  def __init__(self, name, memorized_model_loc, cols_cfg):
    """
    Args:
      name: name of the model.
      memorized_model_loc: location of the memorized model.
      cols_cfg: Name of all the columns used in this model.
    """
    self.name = name
    self.memorized_model_loc = memorized_model_loc
    self.cols_cfg = cols_cfg

class LearnedConfig(object):

  def __init__(self, raw_filenames, feature_map_loc, model_configs):
    """
    Args:
      raw_filenames: List of raw files passed to the LogsToSeti job.
      feature_map_loc: location of where the <feature_name, feature_index> is stored.
      model_cfg: A list of ModelConfig objects, one for each model.
    """
    self.raw_filenames = raw_filenames
    self.feature_map_loc = feature_map_loc
    self.model_configs = model_configs