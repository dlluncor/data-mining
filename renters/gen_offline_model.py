

import logs_to_seti
from ml import learner
from ml import seti

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

def memorize(setis):
  tdg = training_data.TDG()
  blocks = tdg.transform(setis)

def main():
  # Generate an offline model.
  filenames = ['data/tdg_v0.csv']
  #setis = logs_to_seti.generate_seti(filenames)
  setis = [create_seti([('gender', 'm')], [('age', 25)])]
  memorize(setis)
  # Write the model to a file.

main()