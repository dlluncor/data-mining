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
    feature_cols = self.fs.all_col_names
    # Convert SETI inputs into X and y format.
    y = []
    X = []
    for setie in setis:
      x = seti.float_feature_vector(self.fs, setie)
      y.append(setie.label)
      X.append(x)

    lm = LinearRegression()
    lm.fit(X, y)
    #print lm.intercept_
    col_and_coeffs = zip(feature_cols, lm.coef_)
    model = {}
    model[':'] = lm.intercept_
    for (col, coeff) in col_and_coeffs:
      model[col] = coeff
    return model

  def stats(self):
    pass