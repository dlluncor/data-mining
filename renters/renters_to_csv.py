
import datetime
from collections import OrderedDict
from collections import namedtuple

hazards = []
dobs = ['01/10/1990', '10/13/2005', '3/2/2000']


Column = namedtuple('Column', 'values select_type')

d = OrderedDict([
  # header0
  ('Insurance Type', (['Renters'], 'fixed')),
  ('Zip code', (zip_codes, 'fixed')),
  ('First name', (first_names, 'random')),
  ('Last name', (last_names, 'random')),
  ('Date of birth', (dobs, 'iterate')),
  ('Gender', (['m', 'f'], 'random')),
  ('Address', (addresses, 'fixed')),
  ('City', (cities, 'fixed')),
  ('State', (['CA'], 'fixed')),
  ('Zip code', (zip_codes, 'fixed')),
  ('Auto insurance coverage?', (['N'], 'fixed')),
  # header1
  ('Property Type', (['RENTED HOUSE - SINGLE FAMILY'], 'fixed')),
  ('# units', (['1', '2-4', '5+'], 'iterate')),
  ('# unrelated rooomates', (['0', '1', '2', '3 or more'], 'fixed')),
  ('# property losses in last 3 years', (['0', '1', '2', '3', '4', '5 or more'], 'iterate')),
  ('Phone number', (phone_numbers, 'random')),
  ('Email address', (emails, 'random')),
  ('Fire Sprinkler System?', (['Y', 'N'], 'iterate')),
  ('Central Fire & Burglar Alarm?', (['Y', 'N'], 'iterate')),
  ('Local Fire / Smoke Alarm?', (['Y', 'N'], 'iterate')),
  ('Home Security?', (['Y', 'N'], 'iterate')),
  ('Non Smoking Household?', (['Y', 'N'], 'iterate')),
  ('Local Burglar Alarm?', (['Y', 'N'], 'iterate')),
  ('Unusual hazards?', (hazards, 'iterate')),
])



def renter_lines(header):
  # Keep information fixed and then do a search on many parameters.
  # Produce everything based on a fixed information.
  for k, v in d.iteritems():
    k = k
    vc = Column._make(v)
  return ''
  

def get_renters_csv():
  header1 = ['Fire Sprinkler System', 'Central Fire & Burglar Alarm',
             'Local Fire/Smoke Alarm', 'Home Security', 'Non Smoking Household',
             'Local Burglar Alarm',
             'Unusual hazards', 'Dogs that bite', 'Run a business?', 'Start date']
  header2 = ['Personal property worth', 'Loss of use', 'Medical payments',
             'Personal liability', 'Farmers Identity Protection', 'Deductible']
  header = header1 + header2
  lines = []
  lines.append(','.join(header))
  lines += renter_lines(header)
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