import csv, re


def extract_zip_from_address(address):
    m = re.search(r'^(.*), (.*), CA (\d+)', address)
    if m:
        return m.group(1), m.group(2), m.group(3)
    else:
        return (None, None, None)

phone_numbers = []
cities = []
addresses = []
zip_codes = []
with open('apartments_in_ca.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        address = row[1]
        phone_number = row[3]
        if phone_number == '' or not phone_number:
            continue

        address, city, zip_code = extract_zip_from_address(address)

        if not zip_code or not city:
            continue

        address = address.replace("'", '')
        address = address.replace("#", '')
        phone_numbers.append(phone_number)
        cities.append(city)
        addresses.append(address)
        zip_codes.append(zip_code)

        #places.append([zip_code, city, address, phone_number])

#print("cities = ['{}']".format("','".join(cities)))
print("addresses = ['{}']".format("','".join(addresses[:200])))
#print("zip_codes = ['{}']".format("','".join(zip_codes)))
#print("phone_numbers = ['{}']".format("','".join(phone_numbers)))

print(len(phone_numbers))
