"""
   Given a user input, it will determine what is the price given either data memorized from training data
   or a linear regression model if we must estimate given unknown parameters.
"""

class SetiServer(object):

  def __init__(self):
    pass

  def load_model(self, model):
    """Load the model from a file which is really a pickled hashmap."""
    pass

  def score(self, seti):
    """Score the model based on the SETI data."""

    # If we've seen this example before, return the exact price
    # found.
    # Find all feature indices in example.
    # '0-1-2-3-4': 3.0,
    # if we have not seen this example:
    # score using model.
    pass

