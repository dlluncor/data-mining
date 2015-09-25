"""
   Given a user input, it will determine what is the price given either data memorized from training data
   or a linear regression model if we must estimate given unknown parameters.
"""

import math
import csv, seti, model_exporter, model_cfg
import feature_selector

def new_model_scorer(fs2, learned_model):
  ms = _ModelScorer({}, skip_constructor=True)
  ms.fs2 = fs2
  ms.learned_model = learned_model
  ms.model_config = model_cfg.default_model_config()
  return ms

class _ModelScorer(object):

  def __init__(self, model_config, skip_constructor=False):
    """

    """
    if skip_constructor:
      return
    fs2 = feature_selector.FeatureSelect()
    fs2.read_feature_maps(model_config.feature_map2_loc)

    fs = feature_selector.FeatureSelector()
    fs.read_feature_map(model_config.feature_map_loc)
    self.fs = fs  # Not great to pass the feature selector with the loaded feature_index_map in...
    self.fs2 = fs2

    # Model consists of the learned model as well as the memorized model.
    self.model_config = model_config
    self.memorized_prices = self.load_memorized_prices(model_config.memorized_model_loc)
    self.learned_model = self.load_learned_model(model_config.learned_model_loc)

  def load_memorized_prices(self, filename):
    """Load the model from a file which is really a CSV."""
    # Model consists of the learned model as well as the memorized model.
    mm = model_exporter.MemorizedModel()
    return mm.read_features(filename)

  def load_learned_model(self, filename):
    mm = model_exporter.LearnedModel()
    return mm.read_model(filename)

  def get_columns_for_memorization(self):
    return self.model_config.cols_cfg.get_cols_for_memorizing()

  def get_memorized_price(self, seti_input):
    features = seti.create_feature_vector(
      self.fs, self.get_columns_for_memorization(), 
      seti_input)
    key = seti.standard_repr(features)
    #print 'Serving memorized key'
    #print key
    if key in self.memorized_prices:
      return self.memorized_prices[key]
    return None

  def get_learned_price(self, seti_input):
    #print self.learned_model
    yprime = self.learned_model[':']
    vec = seti.to_readable_vector(self.fs2, seti_input)
    #print vec
    for feature_key, feature_val in vec.iteritems():
      val = self.learned_model[feature_key]
      #print val
      yprime += val * feature_val
    if self.model_config.model_type == model_cfg.LOGISTIC_REGRESSION:
      return 1 / (1 + math.exp(-yprime))
    return yprime

def make_from_config(model_configs):
  return SetiServer(model_configs)

class SetiServer(object):

  def __init__(self, model_configs):
    """
      fs: feature_selector.FeatureSelector with all the feature indices.
      fs2: feature_selector.FeatureSelect.
      cols_cfg: Columns to keep.
    """
    self.model_map = {}
    for cfg in model_configs:
      self._load_model_from_config(cfg)

  def _load_model_from_config(self, model_config):
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
    memorized_price = model.get_memorized_price(seti_input)
    if memorized_price is not None:
      return memorized_price
    return model.get_learned_price(seti_input)
