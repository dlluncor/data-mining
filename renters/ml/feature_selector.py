
import csv

class FeatureSelector():

  def __init__(self):
    self.i = 0
    self.feature_to_index = {}

  def build_feature_map(self, setis):
    for seti in setis:
      for bf in seti.bfs:
        if bf in self.feature_to_index:
          # Weve already seen this feature.
          continue
        self.feature_to_index[bf] = self.i
        self.i += 1

      for cf in seti.cfs:
        if cf in self.feature_to_index:
          # Weve already seen this feature.
          continue
        self.feature_to_index[cf.name] = self.i
        self.i += 1

  def write_feature_map(self, fname):
    with open(fname, 'wb') as f: 
      writer = csv.writer(f)
      for k, v in self.feature_to_index.iteritems():
        writer.writerow((k, v))

  def read_feature_map(self, fname):
    f = open(fname, 'r')
    reader = csv.reader(f)
    for k, v in reader:
      self.feature_to_index[k] = v
    f.close()

  def get_index(self, feature):
    if feature not in self.feature_to_index:
      raise Exception('Unrecognized feature not in SETI data: %s' % (feature))
    return self.feature_to_index[feature]