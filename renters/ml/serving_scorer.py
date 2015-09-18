"""
   Given a user input, it will determine what is the price given either data memorized from training data
   or a linear regression model if we must estimate given unknown parameters.
"""

import seti

class SetiServer(object):

  def __init__(self):
    pass

  def load_model(self, model):
    """Load the model from a file which is really a pickled hashmap."""
    # TODO(haoran): Read the memorized model file.
    # Model consists of the learned model as well as the memorized model.
    # E.g., memorized model is 'memorized-v0.pickle'.
    pass

  def score(self, seti_input):
    """Score the model based on the SETI data."""
    
    # If we've seen this example before, return the exact price
    # found.
    # Find all feature indices in example.
    # '0-1-2-3-4': 3.0,
    # if we have not seen this example:
    # score using model.
    features = seti.create_feature_vector(seti_input)
    # TODO(haoran): Determine if the SETI example was already seen and if so
    # return the memorized value for that example.
    pass

