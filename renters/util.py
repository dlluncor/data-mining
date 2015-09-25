import csv, datetime, getopt, json, sys
from collections import Counter

def extract_emails_from_logs():
    emails = Counter()

    for filename in ['data/success_no_0921212303.log', 'data/success_special_0921212303.log']:
        with open(filename) as fin:
            for line in fin:
                log = json.loads(line)
                email = log['data'][16]
                emails[email] += 1
    """
    for filename in ['data/error_no_0921212303.log', 'data/error_special_0921212303.log']:
        with open(filename) as fin:
            for line in fin:
                log = json.loads(line)
                email = log['data'][16]
                if emails[email] > 0:
                    print('Oooops same email scucess and fail; %s' % email)
                    del emails[email]
    """
    print "[%s]" % ','.join( '"%s"' % email for email, cnt in emails.most_common(20))

def convert_and_save(inname, outname):
    with open(inname, 'r') as fin:
        reader = csv.reader(fin)
        reader.next()
        with open(outname, 'a+') as fout:
            writer = csv.writer(fout)
            #writer.writerow(['Insurance Type', 'Zip code', 'First name', 'Last name', 'Date of birth', 'Gender', 'Address', 'City', 'State', 'Auto insurance coverage?', 'Property Type', '# units', '# unrelated roommates', '# property losses in last 3 years', 'Phone number', 'Email address', 'Fire Sprinkler System?', 'Central Fire & Burglar Alarm?', 'Local Fire / Smoke Alarm?', 'Home Security?', 'Non Smoking Household?', 'Local Burglar Alarm?', 'Unusual hazards?', 'Dogs that bite?', 'Run a business from home?', 'Start date', 'Personal property worth', 'Loss of use', 'Medical payments', 'Personal liability', 'Farmers Identity Protection', 'Deductible', 'Policy number', 'Timestamp (seconds)', 'Policy price', 'Name of agent', 'Address of agent', 'Elancer Name'])
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

def convert_files():
    files = ['prices_samples_full_0921212303_0.csv', 'prices_samples_full_0921212303_1.csv',
             'prices_samples_full_0921212303_2.csv', 'prices_samples_full_0921212303_3.csv',
             'prices_samples_full_0921212303_4.csv', 'prices_samples_full_0921212303_5.csv',
             'prices_samples_full_0921212303_6.csv', 'prices_samples_full_0921212303_7.csv',
             'prices_samples_full_0921212303_8.csv', 'prices_samples_full_0921212303_9.csv',
             'prices_samples_full_0921212303_10.csv', 'prices_samples_full_0921212303_11.csv',
             'prices_samples_full_0921212303_12.csv', 'prices_samples_full_0921212303_13.csv']

    outpath = 'data/price_samples_full_0921212303__2.csv'
    with open(outpath, 'w') as fout:
        fout.write("Insurance Type,Zip code,First name,Last name,Date of birth,Gender,Address,City,State,Auto insurance coverage?,Property Type,# units,# unrelated roommates,# property losses in last 3 years,Phone number,Email address,Fire Sprinkler System?,Central Fire & Burglar Alarm?,Local Fire / Smoke Alarm?,Home Security?,Non Smoking Household?,Local Burglar Alarm?,Unusual hazards?,Dogs that bite?,Run a business from home?,Start date,Personal property worth,Loss of use,Medical payments,Personal liability,Farmers Identity Protection,Deductible,Policy number,Timestamp (seconds),Policy price,Name of agent,Address of agent,Elancer\n")

    for fname in files:
        convert_and_save('data/%s' % fname, outpath)

if __name__ == '__main__':
    #extract_emails_from_logs()
    convert_files()
