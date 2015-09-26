import csv

import csv, datetime, getopt, json, sys

def main(argv):
    opts, args = getopt.getopt(argv, 'i:o', ['in=', 'out='])

    inname = None
    outname = None
    for opt, arg in opts:
        if opt in ('-i', '--in'):
            inname = arg
        elif opt in ('-o', '--out'):
            outname = arg

    if inname is None or outname is None:
        print("Usage: -i [input file] -o [out file]")

    with open(inname, 'r') as fin:
        reader = csv.reader(fin)
        reader.next()
        with open(outname, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow(['Insurance Type', 'Zip code', 'First name', 'Last name', 'Date of birth', 'Gender', 'Address', 'City', 'State', 'Auto insurance coverage?', 'Property Type', '# units', '# unrelated roommates', '# property losses in last 3 years', 'Phone number', 'Email address', 'Fire Sprinkler System?', 'Central Fire & Burglar Alarm?', 'Local Fire / Smoke Alarm?', 'Home Security?', 'Non Smoking Household?', 'Local Burglar Alarm?', 'Unusual hazards?', 'Dogs that bite?', 'Run a business from home?', 'Start date', 'Personal property worth', 'Loss of use', 'Medical payments', 'Personal liability', 'Farmers Identity Protection', 'Deductible', 'Policy number', 'Timestamp (seconds)', 'Policy price', 'Name of agent', 'Address of agent', 'Elancer Name'])
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for row in reader:
                (insurance_type, zip_code, first_name, last_name, dob,
                gender, address, city, state, has_auto_insurance_coverage,
                property_type, unit_count, unrelated_roommates_count, roommate_names, property_losses_count, phone_number,
                email, has_fire_sprinkler_system, has_center_fire_burglar_alarm, has_local_fire_smoke_alarm,
                has_home_security, is_non_smoking_household, has_local_burglar_alarm, has_unusual_hazards,
                has_bite_dog, is_running_bussiness, start_date, personal_property_value,
                loss_of_use, medical_payment, personal_liability, farmers_identity_protection,
                deductible, policy_price, annual_policy_price, agent_name, agent_address, agent_phone_number,
                policy_number) = row
                writer.writerow([insurance_type, zip_code, first_name, last_name, dob,
                                gender, address, city, state, has_auto_insurance_coverage,
                                property_type, unit_count, unrelated_roommates_count, property_losses_count, phone_number,
                                email, has_fire_sprinkler_system, has_center_fire_burglar_alarm, has_local_fire_smoke_alarm,
                                has_home_security, is_non_smoking_household, has_local_burglar_alarm, has_unusual_hazards,
                                has_bite_dog, is_running_bussiness, start_date, personal_property_value,
                                loss_of_use, medical_payment, personal_liability, farmers_identity_protection,
                                deductible, policy_number, timestamp, policy_price,
                                agent_name, agent_address, 'haoran'])

if __name__ == '__main__':
  main(sys.argv[1:])
