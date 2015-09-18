







def main():
  # Generate an offline model.
  filenames = ['renters_8000.csv']
  setis = generate_seti(filenames)
  l = Learner(setis)
  l.create_model()
  print l.generate_statistics()
  # Write the model to a file.

main()