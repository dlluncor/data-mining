
import seti_server
import feature_selector
import seti
import model_cfg
import model_exporter
import training_data
import math

def testScoreWithLearnedModel():
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

  model_types = [model_cfg.LINEAR_REGRESSION, model_cfg.LOGISTIC_REGRESSION]
  transforms = [lambda x: x, lambda x: 1 / (1 + math.exp(-x))]

  # Test the actual model.
  for mIndex in xrange(len(model_types)):
    model_config = model_cfg.ModelConfig(
      'v0', 'tmp/learned_model.csv', 'tmp/memorized_model.csv', 
      model_cfg.ColsCfg(orig_cols, orig_cols),
      'tmp/feature_map_v0.csv', 'tmp/feature_map2_v0.csv', 
      model_type=model_types[mIndex])
    training_data.write_feature_maps_from_seti(model_config, setis)

    ss = seti_server.make_from_config([model_config])

    w0 = model[':'] + model['gender_MISSING'] * 0 + model['gender_f'] * 0 + model['height'] * 6.0
    w1 = model[':'] + model['gender_MISSING'] * 0 + model['gender_f'] * 1 + model['height'] * 3.0
    wants = [w0, w1]
    for i in xrange(len(setis)):
      setie = setis[i]
      want_after_transform = transforms[mIndex](wants[i])
      assertEquals(want_after_transform, ss.score(setie))

def testScoreWithMemorizedModel():
  orig_cols = ['gender', 'height']
  memorized_cols = ['gender']
  model_config = model_cfg.ModelConfig(
  'v1', 'tmp/learned_model_v1.csv', 'tmp/memorized_model_v1.csv', 
  model_cfg.ColsCfg(orig_cols, memorized_cols),
  'tmp/feature_map_v1.csv', 'tmp/feature_map2_v1.csv')
  s0 = seti.create_seti(5.0, bfs=[('gender', 'm')], cfs=[('height', 6.0)])
  s1 = seti.create_seti(7.0, bfs=[('gender', 'f')], cfs=[('height', 6.0)])
  setis = [s0, s1]

  # Empty learned model.
  lm = model_exporter.LearnedModel()
  lm.write_model({}, 'tmp/learned_model_v1.csv')

  # Set up memorized model.
  fs, _ = training_data.write_feature_maps_from_seti(model_config, setis)
  mem = model_exporter.Memorizer(fs, model_config)
  memorized_model = mem.create_model(setis)
  mm = model_exporter.MemorizedModel()
  mm.write_features(memorized_model, model_config.memorized_model_loc)

  ss = seti_server.make_from_config([model_config])
  ss.model_map['v1'].learned_model = {}
  s2 = seti.create_seti(7.0, bfs=[('gender', 'f')])
  assertFloatEquals(7.0, ss.score(s2))



# Test util template.
import sys
import inspect

errs = []

def assertFloatEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  v0 = '%.4f' % expected
  v1 = '%.4f' % got
  if v0 != v1:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

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