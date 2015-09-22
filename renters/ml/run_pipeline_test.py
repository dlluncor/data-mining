
import seti_server
import seti
import run_pipeline
import model_cfg

def testRun():
  # Setup feature selector and such.
  orig_cols = ['gender', 'height']

  s0 = seti.create_seti(5.0, bfs=[('gender', 'm')], cfs=[('height', 6.0)])
  s1 = seti.create_seti(3.0, bfs=[('gender', 'f')], cfs=[('height', 3.0)])
  setis = [s0, s1]

  model_config = model_cfg.ModelConfig(
    'v0', 'tmp/learned_model.csv', 'tmp/memorized_model.csv', orig_cols,
    'tmp/feature_map_v0.csv', 'tmp/feature_map2_v0.csv')
  run_pipeline.run([model_config], setis)
  model = { 
    'gender_MISSING': 0.0, 
    'gender_f': -0.099999999999999992, 
    ':': -0.7999999999999996, 
    'height': 0.29999999999999993
  }
  # Test model gets created and loaded.
  # Test that we can score one example.

  ss = seti_server.make_from_config([model_config])
  s2 = seti.create_seti(5.0, bfs=[('gender', 'm')], cfs=[('height', 2.0)])
  val0 = model[':'] + model['gender_MISSING'] * 0 + model['gender_f'] * 0 + model['height'] * 2.0
  assertEquals(val0, ss.score(s2))


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