import csv, time, yelp
from collections import defaultdict

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'ZPqRlJ2RtZDNBSuYTBhsRw'
CONSUMER_SECRET = '0My0ugpbLLROJIL2rJ9LHxv70OA'
TOKEN = 'AuymZLvMMIfLBZSa1yRap6nZaQwD-wvl'
TOKEN_SECRET = 'JQ5TAGWWZkcyg_6y_8g8TSP8pu4'

yelp_api = yelp.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=TOKEN,
                    access_token_secret=TOKEN_SECRET)

apartments = []

def parse_search_result(businesses):
    places = []
    for business in businesses:
        address = business.location.display_address[0]
        city = business.location.city
        full_address = ','.join(business.location.display_address)
        name = business.name
        phone_number = business.display_phone
        rating = business.rating
        review_count = business.review_count
        state = business.location.state_code
        url = business.url
        zip_code = business.location.postal_code


        places.append([name, address, city, state, zip_code, phone_number, full_address, rating, review_count, url])

    return places

def search(term='apartment', location='san francisoco', category='apartments'):
    search_results = yelp_api.Search(term=term, location=location, category_filter=category)
    time.sleep(0) # location and search term are required
    total = search_results.total
    print("total {} businesses for {}".format(total, location))
    offset = 0
    places = parse_search_result(search_results.businesses)

    while offset + len(places) < total:
        offset += len(places)
        try:
            search_results = yelp_api.Search(term=term, location=location, category_filter=category, offset=offset)
            time.sleep(2)
        except Exception as e:
            print("Ooooops exception")
            print(e)

        places = parse_search_result(search_results.businesses)
        if not places:
            print("Oooops no result")
            break

        apartments.extend(places)
        print("get {} places for {}".format(offset + len(places), location))
        save(apartments)

def save(places, name="yelp.csv"):
    if not places:
        print("Empty result. NOT SAVE~")
        return

    with open(name, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Address', 'City', 'State', 'Zip Code', 'Phone Number', 'Full Address', 'Rating', 'Review Count', 'URL'])
        for place in places:
            writer.writerow(place)

def search_all_ca_stations():
    stations = [
                'san francisco', 'bayshore', 'south san francisco', 'san bruno', 'millbrae', 'burlingame',
                'san mateo', 'hayward park', 'hillsdale', 'bellmont', 'san carlos', 'redwood city', 'menlo park',
                'Palo Alto', 'san antionio',
                'mountain view', 'sunnyvale', 'lawrence', 'santa clara',
                'college park', 'san jose diridon', 'tamien', 'capitol', 'blossom hill', 'morgan hill', 'san martin', 'gilroy'
                ]


    for station in stations:
        search(location=station)

def clean_data():
    addresses = defaultdict(lambda: False)
    places = []
    with open('yelp.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, address, city, state, zip_code, phone_number, full_address, rating, review_count, url = row
            if not phone_number:
                print('missing phone number')
                continue

            if addresses[full_address]:
                print("duplicated data:" + address)
                continue
            else:
                places.append(row)
                addresses[full_address] = True

    with open('scrubbed_yelp.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for place in places:
            writer.writerow(place)

clean_data()
print("DONE")
