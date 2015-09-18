

import logs_to_seti





def main():
  # Generate an offline model.
  filenames = ['renters_8000.csv']
  setis = logs_to_seti.generate_seti(filenames)
  l = Learner(setis)
  l.create_model()
  print l.generate_statistics()
  # Write the model to a file.

main()