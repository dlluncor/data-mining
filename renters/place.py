import json, csv, time
from googleplaces import GooglePlaces, GooglePlacesError

KEY = 'AIzaSyD1kCP21v6BwjRxxN8wMYWnBN9zCsxc1zc' # bonjoy
#KEY = 'AIzaSyAw1OBq1qiKcoFDww-kewMQmOzQ75WQFh8' # dennis
#KEY = 'AIzaSyD44mggPK8ZHsbW8GmjuHkjFEqpRePnBGU' # haoran
#KEY = 'AIzaSyAiC-9VXN36C5KWEZjvzbGf_o_VbyEO7-c' # news
place_api = GooglePlaces(KEY)
err_count = 0
places = []
def get_places(location='California', keyword='apartment'):

    next_page_token = None
    while True:
        #results = place_api.nearby_search(location=location, keyword=keyword, pagetoken=next_page_token)
        results = place_api.text_search(location=location, query=keyword, pagetoken=next_page_token)
        next_page_token = results.raw_response.get('next_page_token', None)
        #if next_page_token:
        #    print(json.dumps(results.raw_response, indent=4))

        for place in results.places:
            #print place.name
            #print place.geo_location
            try:
                place.get_details()
                time.sleep(1)
            except GooglePlacesError as e:
                print("got GooglePlacesError and sleep")
                time.sleep(5)
                if err_count > 10:
                    return places
                err_count += 1

            #print place.details
            address = place.details.get('formatted_address', None) or place.details.get('vicinity', None)

            info = {
                'address': address,
                'location': location,
                'name': place.details['name'],
                'phone_number': place.details.get('formatted_phone_number', ''),
                'url': place.details.get('url', ''),
            }
            places.append(info)
        save(places)
        print("get {} places in {} now.".format(len(places), location))
        if not next_page_token:
            break

    return places
    #raw_response = json.loads(results.raw_response)
    #print(results.raw_response['next_page_token'])
    #print(json.dumps(result.raw_response, indent=4))

def save(places, name="out2.csv"):
    if not places:
        return

    print("saving to file")
    with open(name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Name', 'Address', 'Location', 'PhoneNumber', 'URL'])
        for place in places:
            spamwriter.writerow([place['name'], place['address'], place['location'], place['phone_number'], place['url']])

def get_places_by_train_station():
    #http://www.caltrain.com/stations/systemmap.html
    stations = [
                'san francisco', 'bayshore', 'south san francisco', 'san bruno', 'millbrae', 'burlingame',
                'san mateo', 'hayward park', 'hillsdale', 'bellmont', 'san carlos', 'redwood city', 'menlo park',
                'Palo Alto', 'san antionio',
                'mountain view', 'sunnyvale', 'lawrence', 'santa clara',
                'college park', 'san jose diridon', 'tamien', 'capitol', 'blossom hill', 'morgan hill', 'san martin', 'gilroy'
                ]
    try:
        for station in stations:
            location = station + ' ' + 'California'
            get_places(location)
    except Exception as e:
        print(e)
        print("get exception")

get_places_by_train_station()
print("DONE")
