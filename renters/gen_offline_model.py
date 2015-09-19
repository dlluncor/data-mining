import logs_to_seti
from ml import learner
from ml import seti
from ml import feature_selector
from ml import training_data
from ml import memorized_model

def create_seti(bfs, cfs):
  s = seti.SETIExample()
  for bf in bfs:
    s.add_binary(bf[0], bf[1])
  for cf in cfs:
    s.add_continuous(cf[0], cf[1])
  return s

def learn(setis):
  l = learner.Learner()
  l.reset()
  l.learn(setis)
  print 'Model: '
  print l.create_model()
  print 'Statistics: '
  print l.generate_statistics()

def main():
  # - Convert the raw data to SETI.
  filenames = ['data/tdg_v0.csv']
  setis = logs_to_seti.generate_seti(filenames)
  #setis = [create_seti([('gender', 'm')], [('age', 25)])]

  # - Look at the occurence of features and their index.
  fs = feature_selector.FeatureSelector()
  fs.build_feature_map(setis)
  feature_map_loc = 'feature_map_v0.csv'
  fs.write_feature_map(feature_map_loc)

  # - Transform the data to feature vectors.
  tdg = training_data.TDG(fs, ['gender', 'dob'])
  tdg_blocks = tdg.transform(setis)

  fname = 'renters-price-v1.csv'
  mm = memorized_model.Memorizer()
  mm.write_features(tdg_blocks, fname)

  # Write the model to a file.
  print 'Gen offline model'

if __name__ == '__main__':
  main()
