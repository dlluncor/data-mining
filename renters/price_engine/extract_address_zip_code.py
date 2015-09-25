import csv, re


def extract_zip_from_address(address):
    m = re.search(r'^(.*), (.*), CA (\d+)', address)
    if m:
        return m.group(1), m.group(2), m.group(3)
    else:
        return (None, None, None)

# http://ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06085
target_zip_codes = ['94022','94022','94023','94024','94024','94035','94035','94039','94040','94041','94042','94043','94085','94086','94087','94088','94088','94089','94090','94301','94302','94303','94303','94304','94305','94305','94306','94309','94309','94310','95002','95008','95009','95011','95013','95014','95014','95014','95015','95020','95021','95026','95030','95030','95031','95032','95035','95036','95037','95038','95042','95044','95046','95050','95051','95052','95054','95055','95056','95070','95071','95101','95102','95103','95106','95108','95109','95110','95111','95112','95113','95114','95115','95116','95117','95118','95119','95120','95121','95122','95123','95124','95125','95126','95127','95128','95129','95130','95131','95132','95133','95134','95135','95136','95137','95138','95139','95140','95140','95141','95142','95148','95150','95151','95152','95153','95154','95155','95156','95157','95158','95159','95160','95161','95164','95170','95171','95172','95173']
#['94043', '94040', '94044', '94041', '94035', '94039', '94042', '95050', '95051', '95052', '95053', '95054', '95055', '95056']
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

        if not zip_code or not city or zip_code not in target_zip_codes:
            continue

        address = address.replace("'", '')
        address = address.replace("#", '')
        phone_numbers.append(phone_number)
        cities.append(city)
        addresses.append(address)
        zip_codes.append(zip_code)

        #places.append([zip_code, city, address, phone_number])

print("rnd_cities = ['{}']".format("','".join(cities)))
print("rnd_addresses = ['{}']".format("','".join(addresses[:200])))
print("rnd_zip_codes = ['{}']".format("','".join(zip_codes)))
#print("phone_numbers = ['{}']".format("','".join(phone_numbers)))
