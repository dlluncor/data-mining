
import learner
import seti
import feature_selector
import training_data
import model_exporter
import random

def run(model_configs, setis):
  # Determine which setis are for holdout and which are for training.
  for seti in setis:
    if random.random() < 0.1:
      seti.for_holdout = True

  for model_config in model_configs:
    # - Look at the occurence of features and their index.
    fs, fs2 = training_data.write_feature_maps_from_seti(model_config, setis)

    print 'Learning model %s' % (model_config.name)
    # - Memorize the examples.
    mem = model_exporter.Memorizer(fs, model_config)
    memorized_model = mem.create_model(setis)
    mm = model_exporter.MemorizedModel()
    mm.write_features(memorized_model, model_config.memorized_model_loc)
    # - Build a model for unmemorized examples.
    l = learner.Learner(fs2)
    learned_model = l.learn(setis)
    lm = model_exporter.LearnedModel()
    lm.write_model(learned_model, model_config.learned_model_loc)
    print 'Wrote learned model to: %s' % (model_config.learned_model_loc)
    print 'Model performed as: %s' % (str(l.stats()))
    #print l.stats()
    # Write the model to a file.
    print 'Finished model generation for %s' % (model_config.name)