import csv, getopt, json, sys

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

    header = ['Insurance Type', 'Zip code', 'First name', 'Last name', 'Date of birth', 'Gender', 'Address', 'City', 'State', 'Auto insurance coverage?', 'Property Type', '# units', '# unrelated roommates', 'roommate names', '# property losses in last 3 years', 'Phone number', 'Email address', 'Fire Sprinkler System?', 'Central Fire & Burglar Alarm?', 'Local Fire / Smoke Alarm?', 'Home Security?', 'Non Smoking Household?', 'Local Burglar Alarm?', 'Unusual hazards?', 'Dogs that bite?', 'Run a business from home?', 'Start date', 'Personal property worth', 'Loss of use', 'Medical payments', 'Personal liability', 'Farmers Identity Protection', 'Deductible']
    with open(outname, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(header)
        with open(inname, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                writer.writerow(data['data'])

if __name__ == '__main__':
  main(sys.argv[1:])
