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

  def __init__(self, fs):
    self._reset(fs)

  def _reset(self, fs):
    self.fs = fs  # feature_selector.FeatureSelect object.

  def learn(self, setis):
    # Determine the original columns to use.
    feature_cols = self.orig_columns
    # Convert SETI inputs into X and y format.
    y = []
    X = []
    for seti in setis:
      x = feature_vector(self.fs, seti)
      y.append(seti.label)
      X.append(x)

    lm = LinearRegression()
    lm.fit(X, y)
    print lm.intercept_
    col_and_coeffs = zip(feature_cols, lm.coef_)
    model = {}
    model[':'] = lm.intercept_
    for (col, coeff) in col_and_coeffs:
      model[col] = coeff
    return model

  def stats(self):
    pass


def test_learner():
  import feature_selector
  import model_exporter
  import model_cfg
  import serving_scorer
  print 'testing the learner.'
  l = Learner(['gender'])
  s0 = seti.create_seti(1.0, bfs=[('gender', 'm')])
  s1 = seti.create_seti(0.0, bfs=[('gender', 'f')])
  setis = [s0, s1]
  model = l.learn(setis)
  print 'Model: '
  print model

  cfg = model_cfg.ModelConfig(
    name='v1', learned_model_loc='tmp/renters-price-learn-v1.csv', 
    memorized_model_loc = 'tmp/renters-price-v1.csv', cols_cfg=['gender'])

  e = model_exporter.LearnedModel()
  e.write_model(model, 'tmp/renters-price-learn-v1.csv')
  memorized = model_exporter.Memorizer()

  fs = feature_selector.FeatureSelector()
  fs.build_feature_map(setis)

  import training_data
  tdg = training_data.TDG(fs, cfg.cols_cfg)
  tdg_blocks = tdg.transform(setis)
  memorized.write_features(tdg_blocks, 'tmp/renters-price-v1.csv')

  # Write the model to disk.

  # Test what the model actually scores with.
  ss = serving_scorer.SetiServer(fs)
  ss.load_model_from_config(cfg)
  print 'Prediction s0:'
  print ss.score(s0)
  print 'Prediction s1:'
  print ss.score(s1)

if __name__ == '__main__':
  test_learner()