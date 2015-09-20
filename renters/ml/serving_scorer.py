"""
   Given a user input, it will determine what is the price given either data memorized from training data
   or a linear regression model if we must estimate given unknown parameters.
"""

import csv, seti, memorized_model

class _ModelScorer(object):

  def __init__(self, model_config):
    # Model consists of the learned model as well as the memorized model.
    self.model_config = model_config
    self.memorized_prices = self.load_memorized_prices(model_config.memorized_model_loc)

  def load_memorized_prices(self, filename):
    """Load the model from a file which is really a CSV."""
    # Model consists of the learned model as well as the memorized model.
    mm = memorized_model.Memorizer()
    return mm.read_features(filename)

  def get_columns(self):
    return self.model_config.cols_cfg

  def get_memorized_price(self, features):
    key = seti.standard_repr(features)
    if key in self.memorized_prices:
      return self.memorized_prices[key]
    return None

class SetiServer(object):

  def __init__(self, fs):
    """
      fs: feature selector with all the feature indices.
      cols_cfg: Columns to keep.
    """
    self.fs = fs  # Not great to pass the feature selector with the loaded feature_index_map in...
    self.model_map = {}

  def load_model_from_config(self, model_config):
    """Load the model from a file which is really a pickled hashmap."""
    m_scorer = _ModelScorer(model_config)
    if model_config.name in self.model_map:
      raise Exception('Duplicate model being loaded called: %s' % (model_config.name))
    self.model_map[model_config.name] = m_scorer

  def score(self, seti_input, model_name=None):
    """Score the model based on the SETI data."""
    if len(self.model_map) == 0:
      raise Exception('Forgot to load any models!')
    # If we've seen this example before, return the exact price
    # found.
    # Find all feature indices in example.
    # '0-1-2-3-4': 3.0,
    # if we have not seen this example:
    # score using model.
    # Look up which model we are using.
    if model_name is None:
      model_name = self.model_map.keys()[0]

    model = self.model_map[model_name]
    features = seti.create_feature_vector(self.fs, model.get_columns(), seti_input)
    memorized_price = model.get_memorized_price(features)
    if memorized_price is not None:
      return memorized_price
    # TODO(haoran): Determine if the SETI example was already seen and if so
    # return the memorized value for that example.
    pass
