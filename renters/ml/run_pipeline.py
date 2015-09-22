
import learner
import seti
import feature_selector
import training_data
import model_exporter

def run(model_configs, setis):
  for model_config in model_configs:
    # - Look at the occurence of features and their index.
    fs, fs2 = training_data.write_feature_maps_from_seti(model_config, setis)

    print 'Learning model %s' % (model_config.name)
    # - Transform the data to feature vectors.
    tdg = training_data.TDG(fs, model_config.cols_cfg)
    tdg_blocks = tdg.transform(setis)
    # - Memorize the examples.
    mm = model_exporter.MemorizedModel()
    mm.write_features(tdg_blocks, model_config.memorized_model_loc)
    # - Build a model for unmemorized examples.
    l = learner.Learner(fs2)
    learned_model = l.learn(setis)
    print l.stats()
    # Write the model to a file.
    print 'Finished model generation for %s' % (model_config.name)