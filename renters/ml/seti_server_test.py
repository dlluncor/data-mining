
import seti_server
import feature_selector
import seti
import model_cfg
import model_exporter

def testScoreWithModel():
  model = { 
    'gender_MISSING': 0.0, 
    'gender_f': -0.099999999999999992, 
    ':': -0.7999999999999996, 
    'height': 0.29999999999999993
  }
  lm = model_exporter.LearnedModel()
  lm.write_model(model, 'tmp/learned_model.csv')
  mm = model_exporter.MemorizedModel()
  mm.write_features([], 'tmp/memorized_model.csv')
  # Setup feature selector and such.
  orig_cols = ['gender', 'height']

  s0 = seti.create_seti(5.0, bfs=[('gender', 'm')], cfs=[('height', 6.0)])
  s1 = seti.create_seti(3.0, bfs=[('gender', 'f')], cfs=[('height', 3.0)])
  setis = [s0, s1]

  fs2 = feature_selector.FeatureSelect()
  fs2.generate_feature_map(orig_cols, setis)
  #fvs = [[0, 0, 6.0], [0, 1, 3.0]]

  fs = feature_selector.FeatureSelector()
  fs.build_feature_map(setis)

  ss = seti_server.SetiServer(fs, fs2)
  model_config = model_cfg.ModelConfig(
    'v0', 'tmp/learned_model.csv', 'tmp/memorized_model.csv', orig_cols)
  ss.load_model_from_config(model_config)

  w0 = model[':'] + model['gender_MISSING'] * 0 + model['gender_f'] * 0 + model['height'] * 6.0
  w1 = model[':'] + model['gender_MISSING'] * 0 + model['gender_f'] * 1 + model['height'] * 3.0
  wants = [w0, w1]
  for i in xrange(len(setis)):
    setie = setis[i]
    assertEquals(wants[i], ss.score(setie))


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