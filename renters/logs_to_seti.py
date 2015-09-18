"""
  Logs to SETI generates SETI from the logged information (renters CSV).
"""
import csv, renter_form
from feature_extractor import FeatureExtractor
def _to_renter_form(csv_line):
  #   Insurance Type,Zip code,First name,Last name,Date of birth,Gender,Address,City,State,Auto insurance coverage?,Property Type,# units,# unrelated roommates,# property losses in last 3 years,Phone number,Email address,Fire Sprinkler System?,Central Fire & Burglar Alarm?,Local Fire / Smoke Alarm?,Home Security?,Non Smoking Household?,Local Burglar Alarm?,Unusual hazards?,Dogs that bite?,Run a business from home?,Start date,Personal property worth,Loss of use,Medical payments,Personal liability,Farmers Identity Protection,Deductible,Policy number,Timestamp (seconds),Policy price,Name of agent,Address of agent
  (insurance_type, zip_code, first_name, last_name, dob, gender, address, city, state, has_auto_insurance_coverage, property_type, unit_count, unrelated_roommates_count), rest = csv_line[:13], csv_line[13:]
  info = {
    'insurance_type': insurance_type,
    'zip_code': zip_code,
    'first_name': first_name,
    'last_name': last_name,
    'dob': dob,
    'gender': gender,
    'address': address,
    'city': city,
    'state': state,
    'has_auto_insurance_coverage': has_auto_insurance_coverage,
    'property_type': property_type,
    'unit_count': unit_count,
    'unrelated_roommates_count': unrelated_roommates_count,
  }
  return renter_form.RenterForm(info)

def generate_seti(filenames):
  # TODO(haoran): Convert CSV lines to RenterForm.
  setis = []
  # Read each file where each row represents a training example.
  for fname in filenames:
    # Read examples from file.
    with open(fname, 'rb') as csvfile:
      reader = csv.reader(csvfile)
      reader.next() # ignore header
      for csv_line in reader:
          renter_form = _to_renter_form(csv_line)
          fe = FeatureExtractor()
          seti = fe.to_seti(renter_form)
          print(str(seti.__dict__))
          setis.append(seti)
  return setis

if __name__ == '__main__':
    generate_seti(['renters_8000.csv'])
