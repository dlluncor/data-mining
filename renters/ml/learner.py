"""
  A learner takes SETI examples and generates a model from it.

  Implementation is using sklearn:
    http://nbviewer.ipython.org/github/justmarkham/DAT4/blob/master/notebooks/08_linear_regression.ipynb
"""

from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seti_server

import seti

class Learner(object):

  def __init__(self, fs):
    self._reset(fs)

  def _reset(self, fs):
    self.fs = fs  # feature_selector.FeatureSelect object.
    self.holdout_setis = []
    self.model = None

  def learn(self, setis):
    # Determine the original columns to use.
    feature_cols = self.fs.all_col_names
    # Convert SETI inputs into X and y format.
    y = []
    X = []
    for setie in setis:
      if setie.for_holdout:
        self.holdout_setis.append(setie)
        continue
      x = seti.float_feature_vector(self.fs, setie)
      y.append(setie.label)
      X.append(x)

    lm = LinearRegression()
    lm.fit(X, y)
    #print lm.intercept_
    col_and_coeffs = zip(feature_cols, lm.coef_)
    model = {}
    model[':'] = float(lm.intercept_)
    for (col, coeff) in col_and_coeffs:
      model[col] = coeff
    self.model = dict([(k, float(v)) for k, v in model.iteritems()])
    return model

  def stats(self):
    ms = seti_server.new_model_scorer(self.fs, self.model)
    y_true = []
    y_pred = []
    for setie in self.holdout_setis:
      y = ms.get_learned_price(setie)
      actual_y = setie.label
      y_true.append(actual_y)
      y_pred.append(y)
    d = {
      'r2_score' : r2_score(y_true, y_pred),
      'num_holdout': len(self.holdout_setis), 
    }
    return d