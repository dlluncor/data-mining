import csv, pickle

def from_csv_to_pickle():
    with open('data/zip_codes.csv') as fin:
        reader = csv.reader(fin)
        reader.next()
        zip_codes = {}
        for row in reader:
            zip_code, area_code, city, county, state, country = row
            zip_codes[zip_code] = county

        pickle.dump(zip_codes, open('data/zipcodes.p', 'wb'))

if __name__ == '__main__':
    zip_codes = pickle.load( open( "data/zipcodes.p", "rb" ) )
    print(zip_codes)
