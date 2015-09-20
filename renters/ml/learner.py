"""
  A learner takes SETI examples and generates a model from it.

  Implementation is using sklearn:
    http://nbviewer.ipython.org/github/justmarkham/DAT4/blob/master/notebooks/08_linear_regression.ipynb
"""

from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

class Learner(object):

  def __init__(self):
    self.reset()

  def reset(self):
    pass

  def learn(self, tdg_blocks):
    pass

  def stats(self):
    pass


def test_learner():
  'testing the learner.'


if __name__ == '__main__':
  test_learner()