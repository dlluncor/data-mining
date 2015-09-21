import sys, getopt
import renter_constants
from ratings import ratings_to_csv

def main(argv):
  opts, args = getopt.getopt(argv, 'f', ['fake-price'])

  use_fake_prices = False
  for opt, arg in opts:
    if opt in ('-f', '--fake-price'):
      use_fake_prices = True

  if not use_fake_prices:
    print("NOT GENERATE FAKE PRICES")

  w = ratings_to_csv.RequestWriter(
    renter_constants, use_multiple_files=False, use_fake_prices=use_fake_prices)
  w.write()

if __name__ == '__main__':
  main(sys.argv[1:])
