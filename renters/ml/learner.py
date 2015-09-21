"""
  A learner takes SETI examples and generates a model from it.

  Implementation is using sklearn:
    http://nbviewer.ipython.org/github/justmarkham/DAT4/blob/master/notebooks/08_linear_regression.ipynb
"""

from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

import seti

class Learner(object):

  def __init__(self, orig_columns):
    self._reset(orig_columns)

  def _reset(self, orig_columns):
    self.orig_columns = orig_columns

  def feature_vector(self, seti):
    v = []
    for bf in seti.bfs:
      if bf == 'gender:m':
        v.append(0)
      if bf == 'gender:f':
        v.append(1)
    return v

  def learn(self, setis):
    # Determine the original columns to use.
    feature_cols = self.orig_columns
    # Convert SETI inputs into X and y format.
    y = []
    X = []
    for seti in setis:
      x = self.feature_vector(seti)
      y.append(seti.label)
      X.append(x)

    lm = LinearRegression()
    lm.fit(X, y)
    print lm.intercept_
    print zip(feature_cols, lm.coef_)

  def stats(self):
    pass


def test_learner():
  import feature_selector
  import model_exporter
  print 'testing the learner.'
  l = Learner(['gender'])
  s0 = seti.create_seti(1.0, bfs=[('gender', 'm')])
  s1 = seti.create_seti(0.0, bfs=[('gender', 'f')])
  setis = [s0, s1]
  model = l.learn(setis)
  print 'Model: '
  print model

  e = model_exporter.LearnedModel()
  e.write_model(model)

  # Write the model to disk.
  cfg = model_cfg.ModelConfig(
    name='v1', learned_model_loc='tmp/renters-price-learn-v1.csv', 
    memorized_model_loc = 'tmp/renters-price-v1.csv', cols_cfg=['gender'])

  # Test what the model actually scores with.
  fs = feature_selector.FeatureSelector()
  ss = SetiServer(fs)
  ss.load_model_from_config(cfg)
  print ss.score(s0)
  print ss.score(s1)

if __name__ == '__main__':
  test_learner()