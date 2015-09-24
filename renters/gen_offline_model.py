
import logs_to_seti
import renter_constants
from ml import run_pipeline
import sys

_DEBUG = True

def main():
  l_config = renter_constants.learned_config
  if len(sys.argv) == 2:
    # - Convert the raw data to SETI.
    which = sys.argv[1]
    if which == '1':
      l_config = renter_constants.learned_config2
    elif which == '2':
      l_config = renter_constants.learned_config2
      l_config.raw_filenames = ['data/from_haoran/clean_*.csv']
  setis = logs_to_seti.generate_seti(l_config.raw_filenames)
  print 'Generated: %d setis' % len(setis)
  if _DEBUG:
    f = open('tmp/cur_run_setis.csv', 'wb')
    setis_txt = '\n'.join([str(seti) for seti in setis])
    f.write(setis_txt)
    f.close()
    #setis = [create_seti([('gender', 'm')], [('age', 25)])]
  run_pipeline.run(l_config.model_configs, setis)


if __name__ == '__main__':
  main()
