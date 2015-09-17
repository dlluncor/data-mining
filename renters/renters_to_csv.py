
import datetime
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
AddrInfo = namedtuple('AddrInfo', 'use_random shared_random_address_index')

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

    print self.col_name_to_iter_index 

  def get_address_value(self, k, address_info):
    address_info.shared_random_address_index
    cell_value = ''
    addresses = self.constants.rnd_addresses if address_info.use_random else self.constants.addresses
    zip_codes = self.constants.rnd_zip_codes if address_info.use_random else self.constants.zip_codes
    cities = self.constants.rnd_cities if address_info.use_random else self.constants.cities

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
      shared_random_address_index = random_index(self.constants.rnd_addresses)
      address_info = AddrInfo(use_random=True, shared_random_address_index=shared_random_address_index)
      for k, v in self.constants.d.iteritems():
        # This loop chooses the correct value to pick for a particular column in a particular row.
        vc = Column._make(v)
        cell_value = self.get_cell_value(k, vc, address_info, iter_row)
        csv_row.append(cell_value)

      csv_rows.append(','.join(csv_row))

    print len(csv_rows)
    if len(csv_rows) > 1000000:
      raise Exception('Too many permutations to rate!')
    return csv_rows

  def non_cross_products(self):
    # Fill in the values which were not generated in the cross product but we still want to explore the values for.
    # Use default values and fix everything else to the default value when using this particular type.
    cols_not_crossed = set([]) # E.g., {"Address": all_addresses}
    for k, v in self.constants.d.iteritems():
      vc = Column._make(v)
      if vc.select_type == 'fixed' and len(vc.values) > 1:
        cols_not_crossed.add(k)

    print 'Columns not crossed:\n%s' % (str(cols_not_crossed))

    # For all columns that are not crossed, now use all default values and vary just one parameter.
    # We dont need to iterate through all values for Zip code and City since we they are tied to the unique address.
    cols_not_crossed.remove('Zip code')
    cols_not_crossed.remove('City')

    extra_csv_rows = []
    j = 0
    for col_not_crossed in cols_not_crossed:
      column_obj = Column._make(self.constants.d[col_not_crossed])
      all_column_values = column_obj.values
      print 'Column: %s. Num values: %d' % (col_not_crossed, len(all_column_values))
      for i in xrange(1, len(all_column_values)):
        vary_value = all_column_values[i]
        csv_row = []
        shared_random_address_index = random_index(self.constants.addresses)
        # If we are varying the Address, then we need to make sure this index is the same as the vary_value index.
        if col_not_crossed == 'Address':
          shared_random_address_index = i  # Make it equivalent to the index of the address we are varying.

        address_info = AddrInfo(use_random=False, shared_random_address_index=shared_random_address_index)
        # Now construct the row but keep everything default expect for the column we are varying.
        for k, v in self.constants.d.iteritems():
          if k == col_not_crossed:
            # Vary value.
            print 'Vary value: %s %s. row %d' % (k, vary_value, j)
            csv_row.append(vary_value)
          else:
            vc = Column._make(v)
            csv_row.append(self.get_cell_value(k, vc, address_info, iter_row=None))
        extra_csv_rows.append(','.join(csv_row))
        j += 1
    return extra_csv_rows

def write_to_files(prefix, timestamp, rows):
  line_ranges = []
  consumed = 0
  while consumed < len(rows):
    line_ranges.append([consumed, consumed+1250])
    consumed = consumed + 1250
  line_ranges.append([consumed, len(rows)])
  print line_ranges
  #return
  for i in xrange(0, len(line_ranges)):
    line_range = line_ranges[i]
    fname = '%s_renters_%s_%d.csv' % (prefix, timestamp, i)
    fname = fname.replace(' ', '')
    f = open(fname, 'w')
    csv = '\n'.join(rows[line_range[0]:line_range[1]])
    f.write(csv)
    f.close()

class RequestWriter(object):
  """Writes to file all the forms that need to be filled out to build a model of how pricing works."""

  def __init__(self, constants):
    self.timestamp = datetime.datetime.now()
    self.constants = constants

  def get_header(self):
    header = [k for k, v in self.constants.d.iteritems()]
    header += ['Policy number', 'Timestamp (seconds)', 'Policy price', 'Name of agent', 'Address of agent']
    return ','.join(header)

  def write(self):
    # Generate the all cross product rows.
    g = GenRequestLines(self.constants)
    csv_rows = [self.get_header()] + g.all_cross_products()
    print len(csv_rows)
    # Write rows to files.
    write_to_files('full_crosses', self.timestamp, csv_rows)

    # Generate non cross product rows.
    extra_csv_rows = [self.get_header()] + g.non_cross_products()
    print len(extra_csv_rows)
    write_to_files('no_crosses', self.timestamp, extra_csv_rows)

  # Generate special cased cross product rows.

import renter_constants

def main():
  w = RequestWriter(renter_constants)
  w.write()

main()