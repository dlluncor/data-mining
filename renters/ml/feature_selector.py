
import csv
import pickle

# Column -> columns.
# Each column is in an order.
# You fill in the value according to the order of the columns.
# Someone has to read through the SetiInput to determine what all the column
# indices are.
from collections import OrderedDict

class FeatureSelect(object):
  """V2 FeatureSelector. Can be used to determine which features we
  actually need to learn when vectorizing a SetiInput into a list
  of columns for the learner to digest.

  """
  def __init__(self):
    self.bf_col_map = OrderedDict()  # 'dir' -> {'MISSING': True, 'south': True, 'east': True, 'west': True}
    self.cf_col_map = OrderedDict()  # 'dist' -> True (might want to store average values for normalization purposes.)
    self.all_col_names = []

  def write_feature_maps(self, filename):
    container = {
      'bf_col_map': self.bf_col_map,
      'cf_col_map': self.cf_col_map,
      'all_col_names': self.all_col_names
    }
    pickle.dump(container, open(filename, 'wb'))

  def read_feature_maps(self, filename):
    container = pickle.load(open(filename, 'rb'))
    self.bf_col_map = container['bf_col_map']
    self.cf_col_map = container['cf_col_map']
    self.all_col_names = container['all_col_names']

  def generate_feature_map(self, orig_columns, setis):
    cols_to_keep = set(orig_columns)
    # For continuous columns, we just have a 1 - 1 mapping.
    # For binary columns we have a 1 -> many mapping.
    for seti in setis:
      for bf in seti.bfs:
        parts = bf.split(':')
        if len(parts) != 2:
          raise Exception('Seti input cannot have more than one :')
        col, feature_val = parts[0], parts[1]
        if col not in cols_to_keep:
          continue
        # Process this binary feature.
        # Have I seen it already?
        if col not in self.bf_col_map:
          self.bf_col_map[col] = OrderedDict([('MISSING', True)])
        vals_to_info = self.bf_col_map[col]  # This dict keeps track of which col values weve already seen. 
        if feature_val in vals_to_info:
          # No need to process a feature value again. We just need unique ones.
          continue
        vals_to_info[feature_val] = True

      for cf in seti.cfs:
        col = cf.name
        if col not in cols_to_keep:
          continue
        # Process this binary feature.
        # Have I seen it already?
        if col not in self.cf_col_map:
          self.cf_col_map[col] = True

    # All col names are the binary feature column names followed by the continuous feature ones.
    for col, val_to_info in self.bf_col_map.iteritems():
      i = -1
      for val, _ in val_to_info.iteritems():
        i += 1
        if i == 1:
          # Dont add the first feature to this list as a column because it is
          # implicit in how you set all the other values.
          continue
        self.all_col_names.append('%s_%s' % (col, val))

    for col, _ in self.cf_col_map.iteritems():
      self.all_col_names.append(col)

class FeatureSelector():
  """This version of the feature selector counts indices of the features.

   This is used for the memorized model.
  """
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
      self.feature_to_index[k] = int(v)
    f.close()

  def get_index(self, feature):
    if feature not in self.feature_to_index:
      raise Exception('Unrecognized feature not in SETI data: %s' % (feature))
    return self.feature_to_index[feature]