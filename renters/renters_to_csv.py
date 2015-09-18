import renter_constants
from ratings import ratings_to_csv

def main():
  w = ratings_to_csv.RequestWriter(
    renter_constants, use_multiple_files=False, use_fake_prices=True)
  w.write()

main()