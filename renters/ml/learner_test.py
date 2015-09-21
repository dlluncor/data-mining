
import sys
import learner
import inspect
import seti

errs = []

def assertEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  if expected != got:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

"""
Things to consider.
  - Multi-valent columns. (let feature extractor deal with that).
  - Missing columns.
  - Categorical features with many possibilities.
"""

def testFVSimple():
  #print 'testFeatureVector runs.'
  orig_cols = ['gender', 'height']
  l = learner.Learner(orig_cols)
  assertEquals(['gender_MISSING', 'gender_f', 'height'], l.all_col_names)

  s0 = seti.create_seti(1.0, bfs=[('gender', 'm')], cfs=[('height', 6.0)])
  s1 = seti.create_seti(0.0, bfs=[('gender', 'f')], cfs=[('height', 3.0)])
  setis = [s0, s1]
  fvs = [[0, 0, 6.0], [0, 1, 3.0]]
  for i in xrange(len(setis)):
    setie = setis[i]
    fv = fvs[i]
    assertEquals(fv, l.feature_vector(setie))
  
def testFVMissingColumn():
  #print 'testFeatureVector runs.'
  orig_cols = ['gender', 'height']
  l = learner.Learner(orig_cols)
  assertEquals(['gender_MISSING', 'gender_f', 'height'], l.all_col_names)

  s0 = seti.create_seti(1.0, bfs=[], cfs=[('height', 6.0)])
  s1 = seti.create_seti(0.0, bfs=[('gender', 'f')], cfs=[])
  setis = [s0, s1]
  fvs = [[1, 0, 6.0], [0, 1, 0.0]]
  for i in xrange(len(setis)):
    setie = setis[i]
    fv = fvs[i]
    assertEquals(fv, l.feature_vector(setie))

def testFVManyCategorical():
  #print 'testFeatureVector runs.'
  orig_cols = ['dir', 'height']
  l = learner.Learner(orig_cols)
  assertEquals(
    ['dir_MISSING', 'dir_south', 'dir_east', 'dir_west', 'dist'], 
    l.all_col_names)

  s0 = seti.create_seti(1.0, bfs=[('dir', 'north')], cfs=[('dist', 6.0)])
  s1 = seti.create_seti(1.0, bfs=[('dir', 'south')], cfs=[('dist', 5.0)])
  s2 = seti.create_seti(1.0, bfs=[('dir', 'east')], cfs=[('dist', 4.0)])
  s3 = seti.create_seti(1.0, bfs=[('dir', 'west')], cfs=[('dist', 3.0)])
  s4 = seti.create_seti(1.0, bfs=[], cfs=[('dist', 2.0)])
  setis = [s0, s1]
  fvs = [[0, 0, 0, 0, 6.0], [0, 1, 0, 0, 5.0], [0, 0, 1, 0, 4.0],
        [0, 0, 0, 1, 3.0], [1, 0, 0, 0, 3.0]]
  for i in xrange(len(setis)):
    setie = setis[i]
    fv = fvs[i]
    assertEquals(fv, l.feature_vector(setie))


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