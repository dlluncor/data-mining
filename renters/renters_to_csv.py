
import datetime
from collections import OrderedDict
from collections import namedtuple
import renter_constants as c
import itertools
import random

def random_index(l):
  return int(len(l) * random.random())

def pick_from_list(l):
  # Randomly pick from a list.
  return l[random_index(l)]

# We want a type called fixed random. It fixes on the first feature to randomly generates features.
# which are common to that fixed type.

synonyms = {
  '01/10/1990': ['03/08/1990', '04/05/1990', '11/12/1990', '05/06/1989', '02/04/1989', '07/31/1988', '11/18/1989', '12/1/1988', '06/06/1986', '03/27/1987' ,'03/03/1988'],
  '3/2/1994': ['03/08/1994', '04/05/1994', '11/12/1994', '05/06/1994', '02/04/1994', '07/31/1993', '11/18/1993', '12/1/1993', '06/06/1994', '03/27/1994' ,'03/03/1993'],
  '8/8/1940': ['03/08/1940', '04/05/1941', '11/12/1942', '05/06/1950', '02/04/1961', '07/31/1966', '11/18/1970', '12/1/1973', '06/06/1967', '03/27/1954' ,'03/03/1967'],  
}

dobs = ['01/10/1990', '3/2/1994', '8/8/1940']
property_worth = ['4000', '8000', '12000', '16000',
                  '20000','24000', '28000', '32000',
                  '35000', '40000', '50000', '60000', '70000', '80000', '90000', '100000']
loss_of_use = ['Keep default']
medical_payments = ['1000', '2000']
personal_liability = ['100000', '300000', '500000']
deductible = ['100', '100 / 250', '250', '500', '750', '1000', '1500', '2500', '5000']

Column = namedtuple('Column', 'values select_type')
AddrInfo = namedtuple('AddrInfo', 'use_random shared_random_address_index')

use_synonyms_cols = set(['Date of birth'])

# Fixed columns which actually have a list longer than 1 we need to find the values for even though we are not doing
# cross products.
# no_cross_products = 

d = OrderedDict([
  # header0
  ('Insurance Type', (['Renters'], 'fixed')),
  ('Zip code', (c.zip_codes, 'fixed')),
  ('First name', (c.first_names, 'random')),
  ('Last name', (c.last_names, 'random')),
  ('Date of birth', (dobs, 'iterate')),
  ('Gender', (['m', 'f'], 'random')),
  ('Address', (c.addresses, 'fixed')),
  ('City', (c.cities, 'fixed')),
  ('State', (['CA'], 'fixed')),
  ('Zip code', (c.zip_codes, 'fixed')),
  ('Auto insurance coverage?', (['N', 'Y'], 'fixed')), # Y / N
  # header1
  ('Property Type', (['RENTED HOUSE - SINGLE FAMILY'], 'fixed')),
  ('# units', (['1', '2 to 4', '5+'], 'iterate')),
  ('# unrelated roommates', (['0', '1', '2', '3 or more'], 'fixed')),
  ('# property losses in last 3 years', (['0', '1', '2', '3', '4', '5 or more'], 'fixed')), # '0', '1', '2', '3', '4', '5 or more'
  ('Phone number', (c.phone_numbers, 'random')),
  ('Email address', (c.emails, 'random')),
  ('Fire Sprinkler System?', (['N', 'Y'], 'fixed')), # Y / N
  ('Central Fire & Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Local Fire / Smoke Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Home Security?', (['N', 'Y'], 'fixed')), # Y / N
  ('Non Smoking Household?', (['Y', 'N'], 'fixed')), # Y / N
  ('Local Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Unusual hazards?', (['NONE'], 'fixed')),
  ('Dogs that bite?', (['N', 'Y'], 'fixed')), # Y / N
  ('Run a business from home?', (['N'], 'fixed')),
  ('Start date', (['Keep default.'], 'fixed')),
  ('Personal property worth', (property_worth, 'iterate')),
  ('Loss of use', (loss_of_use, 'iterate')),
  ('Medical payments', (medical_payments, 'iterate')),
  ('Personal liability', (personal_liability, 'iterate')),
  ('Farmers Identity Protection', (['N', 'Y'], 'fixed')), # Y / N
  ('Deductible', (deductible, 'iterate'))
])

import pdb

to_check = 105

def renter_lines():

  # Keep information fixed and then do a search on many parameters.
  # Produce everything based on a fixed information.
  iter_col_vals = []
  iter_col_names = []
  col_name_to_iter_index = {}
  i = 0
  for k, v in d.iteritems():
    vc = Column._make(v)
    if vc.select_type != 'iterate':
      continue
    # Find all combinations for these columns.
    iter_col_names.append(k)
    iter_col_vals.append(vc.values)
    col_name_to_iter_index[k] = i
    i += 1
    # For debug purposes.
    if i > to_check:
      break

  print col_name_to_iter_index 

  # Find all combinations of the columns to iterate through.
  iter_col_rows = list(itertools.product(*iter_col_vals))
  #pdb.set_trace()

  def is_address_column(k):
    return k == 'Zip code' or k == 'City' or k == 'Address'

  def get_address_value(k, address_info):
    address_info.shared_random_address_index
    cell_value = ''
    addresses = c.rnd_addresses if address_info.use_random else c.addresses
    zip_codes = c.rnd_zip_codes if address_info.use_random else c.zip_codes
    cities = c.rnd_cities if address_info.use_random else c.cities

    if k == 'Address':
      cell_value = addresses[address_info.shared_random_address_index]
    elif k == 'Zip code':
      cell_value = zip_codes[address_info.shared_random_address_index]
    elif k == 'City':
      cell_value = cities[address_info.shared_random_address_index]
    else:
      raise Exception('Calling get_address_value with non-address column.')
    return cell_value

  def get_cell_value(k, vc, address_info):
    cell_value = ''
    if vc.select_type == 'iterate':
      # For debug purposes.
      if k not in col_name_to_iter_index:
        cell_value = 'N/A'
      else:
        # Pick from the correct index of the iter row.
        col_index = col_name_to_iter_index[k]
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
    if k in use_synonyms_cols:
      cell_value = pick_from_list(synonyms[cell_value])
    # Specifically for addresses we need to randomly group them all together but pick from the same synonym.
    if is_address_column(k):
      cell_value = get_address_value(k, address_info)
    return cell_value

  # Iterate through the columns finding the correct key and then 
  # fill in the fixed or random columns.
  csv_rows = []
  for iter_row in iter_col_rows:
    csv_row = []
    # For each row, some columns need to pick from the same index because they are all dependent. Lets
    # generate a shared_random_index with a fixed length. Specifically just for addresses.
    shared_random_address_index = random_index(c.rnd_addresses)
    address_info = AddrInfo(use_random=True, shared_random_address_index=shared_random_address_index)
    for k, v in d.iteritems():
      # This loop chooses the correct value to pick for a particular column in a particular row.
      vc = Column._make(v)
      cell_value = get_cell_value(k, vc, address_info)
      csv_row.append(cell_value)

    csv_rows.append(','.join(csv_row))

  print len(csv_rows)
  if len(csv_rows) > 1000000:
    raise Exception('Too many permutations to rate!')
  
  # Fill in the values which were not generated in the cross product but we still want to explore the values for.
  # Use default values and fix everything else to the default value when using this particular type.
  cols_not_crossed = set([]) # E.g., {"Address": all_addresses}
  for k, v in d.iteritems():
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
    column_obj = Column._make(d[col_not_crossed])
    all_column_values = column_obj.values
    print 'Column: %s. Num values: %d' % (col_not_crossed, len(all_column_values))
    for i in xrange(1, len(all_column_values)):
      vary_value = all_column_values[i]
      csv_row = []
      shared_random_address_index = random_index(c.addresses)
      # If we are varying the Address, then we need to make sure this index is the same as the vary_value index.
      if col_not_crossed == 'Address':
        shared_random_address_index = i  # Make it equivalent to the index of the address we are varying.

      address_info = AddrInfo(use_random=False, shared_random_address_index=shared_random_address_index)
      # Now construct the row but keep everything default expect for the column we are varying.
      for k, v in d.iteritems():
        if k == col_not_crossed:
          # Vary value.
          print 'Vary value: %s %s. row %d' % (k, vary_value, len(csv_rows) + j)
          csv_row.append(vary_value)
        else:
          vc = Column._make(v)
          csv_row.append(get_cell_value(k, vc, address_info))
      extra_csv_rows.append(','.join(csv_row))
      j += 1

  print len(extra_csv_rows)
  csv_rows += extra_csv_rows
  print len(csv_rows)
  return csv_rows
  

def get_renters_rows():
  header = [k for k, v in d.iteritems()]
  header += ['Policy number', 'Timestamp (seconds)', 'Policy price', 'Name of agent', 'Address of agent']
  lines = []
  lines.append(','.join(header))
  csv_rows = renter_lines()
  lines += csv_rows
  return lines

def main():
  n = datetime.datetime.now()

  rows = get_renters_rows()
  line_ranges = []
  consumed = 0
  #while consumed < len(rows):
  #  line_ranges.append([consumed, consumed+1250])
  #  consumed = consumed + 1250
  line_ranges.append([consumed, len(rows)])
  print line_ranges
  #return
  for i in xrange(0, len(line_ranges)):
    line_range = line_ranges[i]
    fname = 'renters_%s_%d.csv' % (n, i)
    fname = fname.replace(' ', '')
    f = open(fname, 'w')
    csv = '\n'.join(rows[line_range[0]:line_range[1]])
    f.write(csv)
    f.close()

main()