
import logs_to_seti
import renter_constants
from ml import run_pipeline

def main():
  # - Convert the raw data to SETI.
  l_config = renter_constants.learned_config
  setis = logs_to_seti.generate_seti(l_config.raw_filenames)
  #setis = [create_seti([('gender', 'm')], [('age', 25)])]
  run_pipeline.run(l_config, setis) 

if __name__ == '__main__':
  main()
