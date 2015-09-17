
import datetime
from collections import OrderedDict
from collections import namedtuple
import renter_constants as c
import itertools
import random

def pick_from_list(l):
  # Randomly pick from a list.
  i = random.random()
  return l[int(i * len(l))]


dobs = ['01/10/1990', '10/13/2005', '3/2/2000'] # TODO
property_worth = ['4000', '6000', '8000', '10000', '12000', '14000', '16000',
                  '18000', '20000', '22000', '24000', '26000', '28000', '30000',
                  '35000', '40000', '50000', '60000', '70000', '80000', '90000', '100000']
loss_of_use = ['Keep default']
medical_payments = ['1000', '2000']
personal_liability = ['100,000', '300,000', '500,000']
farmers_identity_protection = ['Y', 'N']
deductible = ['100', '100 / 250', '250', '500', '750', '1000', '1500', '2500', '5000']

Column = namedtuple('Column', 'values select_type')

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
  ('# units', (['1', '2-4', '5+'], 'iterate')),
  ('# unrelated rooomates', (['0', '1', '2', '3 or more'], 'fixed')),
  ('# property losses in last 3 years', (['0', '1', '2', '3', '4', '5 or more'], 'iterate')),
  ('Phone number', (c.phone_numbers, 'random')),
  ('Email address', (c.emails, 'random')),
  ('Fire Sprinkler System?', (['Y', 'N'], 'iterate')),
  ('Central Fire & Burglar Alarm?', (['Y', 'N'], 'iterate')),
  ('Local Fire / Smoke Alarm?', (['Y', 'N'], 'iterate')),
  ('Home Security?', (['Y', 'N'], 'iterate')),
  ('Non Smoking Household?', (['Y', 'N'], 'iterate')),
  ('Local Burglar Alarm?', (['Y', 'N'], 'iterate')),
  ('Unusual hazards?', (['NONE'], 'fixed')),
  ('Dogs that bite?', (['Y', 'N'], 'iterate')),
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

to_check = 3

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
  print len(iter_col_rows)
  pdb.set_trace()

  # Iterate through the columns finding the correct key and then 
  # fill in the fixed or random columns.
  csv_rows = []
  for iter_row in iter_col_rows:
    csv_row = []
    for k, v in d.iteritems():
      # For debug purposes.
      if k not in col_name_to_iter_index:
        csv_row.append('N/A')

      vc = Column._make(v)
      if vc.select_type == 'iterate':
        # Pick from the correct index of the iter row.
        col_index = col_name_to_iter_index[k]
        csv_row.append(iter_row[col_index])
      elif vc.select_type == 'fixed':
        # Choose the first element.
        csv_row.append(vc.values[0])
      elif vc.select_type == 'random':
        # Random choose from the list of elements provided in the columns description.
        csv_row.append(pick_from_list(vc.values))
      else:
        panic('Unrecognized type %s' % (vc.select_type))

    csv_rows.append(','.join(csv_row))


  return '\n'.join(csv_rows)
  

def get_renters_csv():
  header = [k for k, v in d.iteritems()]
  lines = []
  lines.append(','.join(header))
  lines += renter_lines()
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