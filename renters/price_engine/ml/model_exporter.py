"""
  Model exporter deals with exporting the model.
"""
import seti, csv

class Memorizer(object):
  """The equivalent of the learned learner."""

  def __init__(self, fs, model_config):
    self.fs = fs
    self.model_config = model_config

  def create_model(self, setis):
    l = []
    for seti_input in setis:
      feature_vector = seti.create_feature_vector(
        self.fs,
        self.model_config.cols_cfg.get_cols_for_memorizing(), seti_input)
      seti_model_key = seti.standard_repr(feature_vector)
      l.append((seti_model_key, seti_input.label))
    return l

class MemorizedModel(object):

  def __init__(self):
    pass

  def write_features(self, memorized_model, filename):
    """
    Args:
      memorized_model: The output of MemorizedModel.create_model.
    """
    with open(filename, 'wb') as fin:
      writer = csv.writer(fin)
      for (seti_model_key, label) in memorized_model:
        row = (seti_model_key, label)
        writer.writerow(row)
    print 'Wrote memorized features to: %s' % (filename)

  def read_features(self, filename):
    prices = {}
    with open(filename, 'rb') as fin:
        reader = csv.reader(fin)
        for key, price in reader:
            prices[key] = float(price)
    return prices

class LearnedModel(object):

  def __init__(self):
    pass

  def write_model(self, model, filename):
    with open(filename, 'wb') as fin:
        writer = csv.writer(fin)
        for key, weight in model.iteritems():
          row = (key, weight)
          writer.writerow(row)

  def read_model(self, filename):
    m = {}
    print 'read_model learned'
    with open(filename, 'rb') as fin:
        reader = csv.reader(fin)
        for key, weight in reader:
            m[key] = float(weight)
    return m
