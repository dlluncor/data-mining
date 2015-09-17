
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
personal_liability = ['100,000', '300,000', '500,000']
farmers_identity_protection = ['N'] # Y / N
deductible = ['100', '100 / 250', '250', '500', '750', '1000', '1500', '2500', '5000']

Column = namedtuple('Column', 'values select_type')

use_synonyms_cols = set(['Date of birth'])

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
  ('Auto insurance coverage?', (['N'], 'fixed')),
  # header1
  ('Property Type', (['RENTED HOUSE - SINGLE FAMILY'], 'fixed')),
  ('# units', (['1', '2 to 4', '5+'], 'iterate')),
  ('# unrelated rooomates', (['0', '1', '2', '3 or more'], 'fixed')),
  ('# property losses in last 3 years', (['0'], 'iterate')), # '0', '1', '2', '3', '4', '5 or more'
  ('Phone number', (c.phone_numbers, 'random')),
  ('Email address', (c.emails, 'random')),
  ('Fire Sprinkler System?', (['N'], 'iterate')), # Y / N
  ('Central Fire & Burglar Alarm?', (['N'], 'iterate')), # Y / N
  ('Local Fire / Smoke Alarm?', (['N'], 'iterate')), # Y / N
  ('Home Security?', (['N'], 'iterate')), # Y / N
  ('Non Smoking Household?', (['Y'], 'iterate')), # Y / N
  ('Local Burglar Alarm?', (['N'], 'iterate')), # Y / N
  ('Unusual hazards?', (['NONE'], 'fixed')),
  ('Dogs that bite?', (['N'], 'iterate')), # Y / N
  ('Run a business from home?', (['N'], 'fixed')),
  ('Start date', (['Keep default.'], 'fixed')),
  ('Personal property worth', (property_worth, 'iterate')),
  ('Loss of use', (loss_of_use, 'iterate')),
  ('Medical payments', (medical_payments, 'iterate')),
  ('Personal liability', (personal_liability, 'iterate')),
  ('Farmers Identity Protection', (farmers_identity_protection, 'iterate')),
  ('Deductible', (deductible, 'iterate')),
  #('', ([], '')),
  #('', ([], '')),
])

import pdb

to_check = 105

def renter_lines():
  # TODO(dlluncor): Need to have a type which is not only fixed, but you use the default value
  # and you ask for its value when not crossed with any other parameters.

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
  print len(iter_col_rows)
  if len(iter_col_rows) > 1000000:
    panic('Too many permutations to rate!')
  #pdb.set_trace()

  # Iterate through the columns finding the correct key and then 
  # fill in the fixed or random columns.
  csv_rows = []
  for iter_row in iter_col_rows:
    csv_row = []
    # For each row, some columns need to pick from the same index because they are all dependent. Lets
    # generate a shared_random_index with a fixed length. Specifically just for addresses.
    shared_random_address_index = random_index(c.rnd_addresses)
    for k, v in d.iteritems():
      # This loop chooses the correct value to pick for a particular column in a particular row.
      vc = Column._make(v)
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
      if k == 'Address':
        cell_value = c.rnd_addresses[shared_random_address_index]
      elif k == 'Zip code':
        cell_value = c.rnd_zip_codes[shared_random_address_index]
      elif k == 'City':
        cell_value = c.rnd_cities[shared_random_address_index]
      csv_row.append(cell_value)

    csv_rows.append(','.join(csv_row))


  return '\n'.join(csv_rows)
  

def get_renters_csv():
  header = [k for k, v in d.iteritems()]
  lines = []
  lines.append(','.join(header))
  lines.append(renter_lines())
  return '\n'.join(lines)


def main():
  n = datetime.datetime.now()
  fname = 'renters_%s.csv' % (n)
  fname = fname.replace(' ', '')
  f = open(fname, 'w')
  csv = get_renters_csv()
  f.write(csv)
  f.close()

main()