"""
  A learner takes SETI examples and generates a model from it.
"""

from sklearn.linear_model import LinearRegression

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