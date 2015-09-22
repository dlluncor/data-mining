
import seti
import feature_selector
import learner

def testLearn():
  orig_cols = ['gender', 'height']

  s0 = seti.create_seti(1.0, bfs=[('gender', 'm')], cfs=[('height', 6.0)])
  s1 = seti.create_seti(0.0, bfs=[('gender', 'f')], cfs=[('height', 3.0)])
  setis = [s0, s1]

  fs = feature_selector.FeatureSelect()
  fs.generate_feature_map(orig_cols, setis)
  fvs = [[0, 0, 6.0], [0, 1, 3.0]]

  l = learner.Learner(fs)
  print l.learn(setis)


# Test util template.
import sys
import inspect

errs = []

def assertEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  if expected != got:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

def main():
  funs = dir(sys.modules[__name__])
  for fun in funs:
    if fun.startswith('test'):
      globals()[fun]()
  if len(errs) == 0:
    print '%s test passes!' % (sys.argv[0])
  else:
    for err in errs:
      print err
  
if __name__ == '__main__':
  main()