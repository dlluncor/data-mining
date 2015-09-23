#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
  Logs to SETI generates SETI from the logged information (renters CSV).
"""

import csv, renter_form
from feature_extractor import FeatureExtractor
import glob

_DEBUG = False

NUM_COLS = 38

def _to_renter_form(csv_line):
  if len(csv_line) != NUM_COLS:
    raise Exception('csv_line is length: %d. Needs to be %d' % (len(csv_line), NUM_COLS))
  #   Insurance Type,Zip code,First name,Last name,Date of birth,Gender,Address,City,State,Auto insurance coverage?,Property Type,# units,# unrelated roommates,# property losses in last 3 years,Phone number,Email address,Fire Sprinkler System?,Central Fire & Burglar Alarm?,Local Fire / Smoke Alarm?,Home Security?,Non Smoking Household?,Local Burglar Alarm?,Unusual hazards?,Dogs that bite?,Run a business from home?,Start date,Personal property worth,Loss of use,Medical payments,Personal liability,Farmers Identity Protection,Deductible,Policy number,Timestamp (seconds),Policy price,Name of agent,Address of agent
  # 37 columns.
  ( # 5
    insurance_type, zip_code, first_name, last_name, dob,
    gender, address, city, state, has_auto_insurance_coverage,
    property_type, unit_count, unrelated_roommates_count, property_losses_count, phone_number,
    # 4
    email, has_fire_sprinkler_system, has_center_fire_burglar_alarm, has_local_fire_smoke_alarm,
    has_home_security, is_non_smoking_household, has_local_burglar_alarm, has_unusual_hazards, 
    has_bite_dog, is_running_bussiness, start_date, personal_property_value, 
    loss_of_use, medical_payment, personal_liability, farmers_identity_protection, 
    deductible, policy_number, timestamp, policy_price, 
    agent_name, agent_address, elancer_name) = csv_line
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
    'policy_price': policy_price,
  }
  form = renter_form.RenterForm(info)
  policy_price, err = form.get_policy_price()
  if policy_price is None:
    return None, err
  form.label = policy_price
  return form, None

def is_bad_line(line):
  """Validate line and make sure all fields are filled in.

  """
  if len(line) != NUM_COLS:
    return True, 'Length is not %d. Its %d' % (NUM_COLS, len(line))
  i = 0
  for el in line:
    if el == '':
      return True, 'Empty character in column %d' % i
    i += 1
  return False, None

def generate_seti(filenames):
  files = []
  for filename in filenames:
    for fname in glob.glob(filename):
      files.append(fname)
  print 'logs_to_seti reading from files: %s' % (str(files))
  setis = []
  # Read each file where each row represents a training example.
  for fname in files:
    num_lines = 0
    num_invalid_lines = 0
    num_bad_entry_lines = 0
    bad_entry_lines = []
    # Read examples from file.
    with open(fname, 'rb') as csvfile:
      reader = csv.reader(csvfile)
      reader.next() # ignore header
      i = 0
      invalid_lines = []
      for csv_line in reader:
        num_lines += 1
        bad_line, reason = is_bad_line(csv_line)
        if bad_line:
          num_invalid_lines += 1
          continue
        #try:
        renter_form, err = _to_renter_form(csv_line)
        if renter_form is None:
          print err
          num_bad_entry_lines += 1
          bad_entry_lines.append(csv_line)
          continue
        fe = FeatureExtractor()
        seti = fe.to_seti(renter_form)
        setis.append(seti)
        #except Exception as e:
        #  num_invalid_lines += 1
        #  invalid_lines.append(i)
        #  print 'e: %s' % (str(e))
        #  PrintException()
        #  print 'Could not parse line %d. %d cols. \n%s' % (i, len(csv_line), csv_line)
        i += 1
    # Finished handling file.
    print 'File: %s' % fname
    valid_lines = num_lines-num_invalid_lines-num_bad_entry_lines
    print 'Num lines: %d. Valid: %d. Invalid: %d. Bady entry: %d' % (num_lines, valid_lines, num_invalid_lines, num_bad_entry_lines)

  if len(setis) == 0:
    raise Exception('No setis generated!')
  return setis

if __name__ == '__main__':
    #generate_seti(['renters_8000.csv'])
    generate_seti(['data/tdg_v0.csv'])
