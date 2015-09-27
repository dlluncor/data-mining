import csv, json, sys

def extract(src_path, dst_path):
    with open(dst_path, 'wb') as fout:
        writer = csv.writer(fout)
        # add header
        header = 'Insurance Type,Zip code,First name,Last name,Date of birth,Gender,Address,City,State,Auto insurance coverage?,Property Type,# units,# unrelated roommates,roommate names,# property losses in last 3 years,Phone number,Email address,Fire Sprinkler System?,Central Fire & Burglar Alarm?,Local Fire / Smoke Alarm?,Home Security?,Non Smoking Household?,Local Burglar Alarm?,Unusual hazards?,Dogs that bite?,Run a business from home?,Start date,Personal property worth,Loss of use,Medical payments,Personal liability,Farmers Identity Protection,Deductible'
        writer.writerow(header.split(','))
        with open(src_path, 'rb') as fin:
            for line in fin:
                record = json.loads(line)
                row = record['data']
                writer.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("Usage: python program src_path dst_path")

    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    extract(src_path, dst_path)
