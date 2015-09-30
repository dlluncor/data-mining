set -e
#set -x

BASE_URL=http://localhost:8888
#BASE_URL=http://immense-badlands-3000.herokuapp.com

# Test valid card
echo 'Test Valid Card'
curl -X POST -d "number=4111111111111111&expiration_date=10/24&cvv=1234" $BASE_URL/credit_cards
# Test Card with invalid number
curl -X POST -d "number=4111111111111112&expiration_date=10/24&cvv=1234" $BASE_URL/credit_cards
# Test Expired Card
curl -X POST -d "number=4111111111111111&expiration_date=10/14&cvv=1234" $BASE_URL/credit_cards
# Test Card with invalid cvv
curl -X POST -d "number=4111111111111111&expiration_date=10/14&cvv=123" $BASE_URL/credit_cards
