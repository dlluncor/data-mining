"""
   Given a user input, it will determine what is the price given either data memorized from training data
   or a linear regression model if we must estimate given unknown parameters.
"""

import csv, seti, memorized_model

class SetiServer(object):

  def __init__(self, fs, cols_cfg):
    """
      fs: feature selector with all the feature indices.
      cols_cfg: Columns to keep.
    """
    self.fs = fs  # Not great to pass the feature selector with the loaded feature_index_map in...
    self.cols_cfg = cols_cfg
    self.memorized_prices = None
    self.model = None

  def load_memorized_prices(self, filename):
    """Load the model from a file which is really a CSV."""
    # Model consists of the learned model as well as the memorized model.
    mm = memorized_model.Memorizer()
    return mm.read_features(filename)

  def load_model(self, pricefile, modelfile=None):
    """Load the model from a file which is really a pickled hashmap."""
    # TODO(haoran): Read the memorized model file.
    # Model consists of the learned model as well as the memorized model.
    # E.g., memorized model is 'memorized-v0.pickle'.
    self.memorized_prices = self.load_memorized_prices(pricefile)
    # TODO load model from file

  def score(self, seti_input):
    """Score the model based on the SETI data."""

    # If we've seen this example before, return the exact price
    # found.
    # Find all feature indices in example.
    # '0-1-2-3-4': 3.0,
    # if we have not seen this example:
    # score using model.
    features = seti.create_feature_vector(self.fs, self.cols_cfg, seti_input)
    key = seti.standard_repr(features)
    if key in self.memorized_prices:
        return self.memorized_prices[key]
    # TODO(haoran): Determine if the SETI example was already seen and if so
    # return the memorized value for that example.
    pass
