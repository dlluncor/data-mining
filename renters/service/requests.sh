set -e
#set -x

BASE_URL=http://localhost:8080
#BASE_URL=http://immense-badlands-3000.herokuapp.com

# Test when the user wants to know the price of the insurance.
curl -H "Content-Type: application/json" -X POST -d  '
{
    "renter_form": {
       "insurance_type": "Renters",
       "first_name": "Christian",
       "last_name": "Bale",
       "dob": "01/30/1974",
       "gender": "m",
       "address": "3328 Bay Road",
       "city": "Rewood City",
       "state": "CA",
       "zip_code": "94063",
       "purchase_category": "cheap"
    }
}' \
$BASE_URL/price

printf '\n-----------------------------------\n'

# Test when the user purchases insurance.
curl -H "Content-Type: application/json" -X POST -d  '
{
    "renter_form": {
       "insurance_type": "Renters",
       "first_name": "Christian",
       "last_name": "Bale",
       "dob": "01/30/1974",
       "gender": "m",
       "address": "3328 Bay Road",
       "city": "Rewood City",
       "state": "CA",
       "zip_code": "94063",
       "purchase_category": "medium"
    }
}' \
$BASE_URL/buy