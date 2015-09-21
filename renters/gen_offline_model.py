import logs_to_seti
from ml import learner
from ml import seti
from ml import feature_selector
from ml import training_data
from ml import model_exporter

import renter_constants

def main():
  # - Convert the raw data to SETI.
  l_config = renter_constants.learned_config
  setis = logs_to_seti.generate_seti(l_config.raw_filenames)
  #setis = [create_seti([('gender', 'm')], [('age', 25)])]

  # - Look at the occurence of features and their index.
  fs = feature_selector.FeatureSelector()
  fs.build_feature_map(setis)
  fs.write_feature_map(l_config.feature_map_loc)

  for model_config in l_config.model_configs:
    print 'Learning model %s' % (model_config.name)
    # - Transform the data to feature vectors.
    tdg = training_data.TDG(fs, model_config.cols_cfg)
    tdg_blocks = tdg.transform(setis)
    # - Memorize the examples.
    mm = model_exporter.Memorizer()
    mm.write_features(tdg_blocks, model_config.memorized_model_loc)
    # - Build a model for unmemorized examples.
    l = learner.Learner()
    learned_model = l.learn(setis)
    print l.stats()
    # Write the model to a file.
    print 'Finished model generation for %s' % (model_config.name)

if __name__ == '__main__':
  main()
