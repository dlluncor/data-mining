
import logs_to_seti
import renter_constants
from ml import run_pipeline
from ml import model_cfg
import sys

_DEBUG = True

def main(argv):
  l_config = renter_constants.learned_config
  if len(argv) == 2:
    # - Convert the raw data to SETI.
    which = argv[1]
    if which == '1':
      l_config = renter_constants.learned_config2
    elif which == '2':
      l_config = renter_constants.learned_config2
      l_config.raw_filenames = ['data/from_haoran/clean_*.csv']
    elif which == '3' or which =='regression_test':
      l_config = renter_constants.learned_config2
      l_config.raw_filenames = ['data/price_samples_full_0921212303.csv']
      if which == 'regression_test':
        model_cfg.change_dirs('tmp/regression_test', l_config.model_configs)
  setis = logs_to_seti.generate_seti(l_config.raw_filenames)
  #setis = setis[0:1000]
  print 'Generated: %d setis' % len(setis)
  if _DEBUG:
    f = open('tmp/cur_run_setis.csv', 'wb')
    setis_txt = '\n'.join([str(seti) for seti in setis])
    f.write(setis_txt)
    f.close()
  run_pipeline.run(l_config.model_configs, setis)
  return {
    'setis': setis,
    'l_config': l_config
  }


if __name__ == '__main__':
  main(sys.argv)
