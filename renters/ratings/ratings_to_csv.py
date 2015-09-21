import datetime
from ml import common
from collections import OrderedDict
from collections import namedtuple
import itertools
import random

def random_index(l):
  return int(len(l) * random.random())

def pick_from_list(l):
  # Randomly pick from a list.
  return l[random_index(l)]

# We want a type called fixed random. It fixes on the first feature to randomly generates features.
# which are common to that fixed type.

Column = namedtuple('Column', 'values select_type')
AddrInfo = namedtuple('AddrInfo', 'vary_column shared_random_address_index')

import pdb

def is_address_column(k):
  return k == 'Zip code' or k == 'City' or k == 'Address'

class GenRequestLines(object):
  """This class generates what fields need to be filled out for a particular form; Output is in CSV."""

  def __init__(self, constants):
    self.constants = constants
    # Keep information fixed and then do a search on many parameters.
    # Produce everything based on a fixed information.
    self.iter_col_vals = []
    self.iter_col_names = []
    self.col_name_to_iter_index = {}
    i = 0
    for k, v in self.constants.d.iteritems():
      vc = Column._make(v)
      if vc.select_type != 'iterate':
        continue
      # Find all combinations for these columns.
      self.iter_col_names.append(k)
      self.iter_col_vals.append(vc.values)
      self.col_name_to_iter_index[k] = i
      i += 1
      # For debug purposes.
      #if i > to_check:
      #  break

    print 'Col name to iterate index:'
    print self.col_name_to_iter_index

  def make_addr_info(self, vary_column, shared_random_address_index=None):
    """If True, then vary_column the Address column."""
    #rnd_addresses confusingly == vary_column = False
    #adddresses == vary_column = True
    if shared_random_address_index is None:
      if vary_column:
        # If the address is involved in the cross, make sure to construct the proper
        shared_random_address_index = random_index(self.constants.addresses)
      else:
        shared_random_address_index = random_index(self.constants.rnd_addresses)
    return AddrInfo(vary_column=vary_column, shared_random_address_index=shared_random_address_index)

  def get_address_value(self, k, address_info):
    address_info.shared_random_address_index
    cell_value = ''
    addresses = self.constants.addresses if address_info.vary_column else self.constants.rnd_addresses
    zip_codes = self.constants.zip_codes if address_info.vary_column else self.constants.rnd_zip_codes
    cities = self.constants.cities if address_info.vary_column else self.constants.rnd_cities

    if k == 'Address':
      cell_value = addresses[address_info.shared_random_address_index]
    elif k == 'Zip code':
      cell_value = zip_codes[address_info.shared_random_address_index]
    elif k == 'City':
      cell_value = cities[address_info.shared_random_address_index]
    else:
      raise Exception('Calling get_address_value with non-address column.')
    return cell_value

  def get_cell_value(self, k, vc, address_info, iter_row):
    cell_value = ''
    if vc.select_type == 'iterate':
      # For debug purposes.
      if k not in self.col_name_to_iter_index:
        cell_value = 'N/A'
      else:
        # Pick from the correct index of the iter row.
        col_index = self.col_name_to_iter_index[k]
        if iter_row is None:
          # That means we want to grab a default cell_value and we are not looking through all permutations.
          cell_value = vc.values[0]
        else:
          cell_value = iter_row[col_index]
    elif vc.select_type == 'fixed':
      # Choose the first element.
      cell_value = vc.values[0]
    elif vc.select_type == 'random':
      # Random choose from the list of elements provided in the columns description.
      cell_value = pick_from_list(vc.values)
    else:
      panic('Unrecognized type %s' % (vc.select_type))

    # This block is all synonym logic so we dont get detected that all addresses and DOB look the same. But we want
    # it fixed because these columns affect price.
    # Find synonyms for the cell value before emitting if we need to.
    if k in self.constants.use_synonyms_cols:
      cell_value = pick_from_list(self.constants.synonyms[cell_value])
    # Specifically for addresses we need to randomly group them all together but pick from the same synonym.
    if is_address_column(k):
      cell_value = self.get_address_value(k, address_info)
    return cell_value

  def all_cross_products(self):
    # Find all combinations of the columns to iterate through.
    iter_col_rows = list(itertools.product(*self.iter_col_vals))
    #pdb.set_trace()

    # Iterate through the columns finding the correct key and then
    # fill in the fixed or random columns.
    csv_rows = []
    for iter_row in iter_col_rows:
      csv_row = []
      # For each row, some columns need to pick from the same index because they are all dependent. Lets
      # generate a shared_random_index with a fixed length. Specifically just for addresses.
      address_info = self.make_addr_info(vary_column=False)
      for k, v in self.constants.d.iteritems():
        # This loop chooses the correct value to pick for a particular column in a particular row.
        vc = Column._make(v)
        cell_value = self.get_cell_value(k, vc, address_info, iter_row)
        csv_row.append(cell_value)

      csv_rows.append(','.join(csv_row))

    if len(csv_rows) > 1000000:
      raise Exception('Too many permutations to rate!')
    return csv_rows

  def non_cross_products(self):
    # Fill in the values which were not generated in the cross product but we still want to explore the values for.
    # Use default values and fix everything else to the default value when using this particular type.
    cols_not_crossed = set([]) # E.g., {"Address": all_addresses}
    single_cross_cfgs = []
    for k, v in self.constants.d.iteritems():
      if k == 'Zip code' or k == 'City':
        # For all columns that are not crossed, now use all default values and vary just one parameter.
        # We dont need to iterate through all values for Zip code and City since we they are tied to the unique address.
        continue
      vc = Column._make(v)
      if vc.select_type == 'fixed' and len(vc.values) > 1:
        cross_cfg = ([k])
        single_cross_cfgs.append(cross_cfg)
        #cols_not_crossed.add(k)
    return self.special_cross_products(single_cross_cfgs, vary_address=True)
    #print 'Columns not crossed:\n%s' % (str(cols_not_crossed))

  def special_cross_products(self, cross_cfgs, vary_address=False):
    """Find cross products which are specified in the config."""

    # Find which crosses need to be changed, and then generate the other fields as needed.
    # crosses = [{'Date': 'value', 'Last name': 'Smith'}, ...]
    # generate cell_value with iter_row = None.
    value_crosses = []
    for cfg in cross_cfgs:
      value_lists = []
      index_to_col_name = {}
      cross_cfg = common.CrossConfig(cfg)
      #print 'Cross config: '
      #print cross_cfg
      for i in xrange(0, len(cross_cfg.columns)):
        column = cross_cfg.columns[i]
        v = self.constants.d[column]
        vc = Column._make(v)
        value_lists.append(vc.values)
        index_to_col_name[i] = column
      # Now value lists contains all possible values for the crosses. Now find all combinations here.
      #print 'All values stored in the list:'
      #print value_lists
      all_possible_value_combos = list(itertools.product(*value_lists))
      for value_combo in all_possible_value_combos:
        value_cross = {}
        for col_index in xrange(0, len(value_combo)):
          # Simply get the actual value from the value list and get which column it came from.
          value_cross[index_to_col_name[col_index]] = value_combo[col_index]
        value_crosses.append(value_cross)

    #print 'Value crosses: '
    #print value_crosses
    csv_rows = []
    for cross in value_crosses:
      csv_row = []
      # An address should never be involved in a cross, for now.
      shared_index = None
      if 'Address' in cross:
        if vary_address == False:
          raise Exception('Cannot include Address in a cross AND vary the address. It must be static.')
        shared_index = self.constants.addresses.index(cross['Address'])
      address_info = self.make_addr_info(vary_address, shared_random_address_index=shared_index)

      for k, v in self.constants.d.iteritems():
        if k in cross:
          # Use the cross value.
          #print 'Cross: %s' % (str(cross[k]))
          csv_row.append(cross[k])
        else:
          # Use a default value since we are not varying this parameter.
          val = self.get_cell_value(k, Column._make(v), address_info, iter_row=None)
          csv_row.append(val)
      csv_rows.append(','.join(csv_row))

    return csv_rows

# The columns that will be filled in by the mechanical turkers.
faked_d = OrderedDict([
  ('Policy number', ['1234', '5678', '91011']),
  ('Timestamp (seconds)', ['Sat', 'Mon', 'Tues']),
  ('Policy price', ['%.2f' % (15 + random.random() * 30) for i in xrange(100)]),
  ('Name of agent', ['Patricia Ag', 'Martha Ag', 'John Ag']),
  ('Address of agent', ['Mtv', 'Cupertino', 'Redwood City']),
])

class RequestWriter(object):
  """Writes to file all the forms that need to be filled out to build a model of how pricing works."""

  def __init__(self, constants, use_multiple_files, use_fake_prices):
    self.timestamp = datetime.datetime.now().strftime('%m%d%H%M%S')
    self.constants = constants
    self.use_multiple_files = use_multiple_files
    self.use_fake_prices = use_fake_prices

  def get_header(self):
    header = [k for k, v in self.constants.d.iteritems()]
    if self.use_fake_prices:
        header += faked_d.keys()
    return ','.join(header)

  def write_to_files(self, prefix, orig_rows):
    rows = orig_rows
    if self.use_fake_prices:
      rows = []
      # Write the fake results of what gets appended to the header for training data purposes.
      i = -1
      for orig_row in orig_rows:
        i += 1
        new_row = []
        new_row.append(orig_row)
        if i != 0:
          # Add fake items to the non-header row.
          for k, v in faked_d.iteritems():
            value = pick_from_list(v)
            new_row.append(value)
        rows.append(','.join(new_row))

    line_ranges = []
    consumed = 0
    if self.use_multiple_files:
      while consumed < len(rows):
        line_ranges.append([consumed, consumed + 1250])
        consumed = consumed + 1250
    else:
      self.timestamp = ''
    line_ranges.append([consumed, len(rows)])
    print(line_ranges)
    # print line_ranges
    #return
    for i in xrange(0, len(line_ranges)):
      line_range = line_ranges[i]
      csv = '\n'.join(rows[line_range[0]:line_range[1]])
      if csv == '':
        continue
      fname = '%s_renters_%s_%d.csv' % (prefix, self.timestamp, i)
      fname = fname.replace(' ', '')
      print 'Wrote csv request file to %s' % (fname)
      f = open(fname, 'w')
      f.write(csv)
      f.close()

  def write(self):
    g = GenRequestLines(self.constants)

    # Generate the all cross product rows.
    csv_rows = [self.get_header()] + g.all_cross_products()
    print len(csv_rows)
    self.write_to_files('full_crosses', csv_rows)

    # Generate non cross product rows.
    extra_csv_rows = [self.get_header()] + g.non_cross_products()
    print len(extra_csv_rows)
    self.write_to_files('no_crosses', extra_csv_rows)

    # Generate special cased cross product rows.
    rows_3 = [self.get_header()] + g.special_cross_products(self.constants.special_cross_cfgs)
    print len(rows_3)
    self.write_to_files('special_crosses', rows_3)
