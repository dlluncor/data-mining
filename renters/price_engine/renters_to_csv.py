import sys, getopt
import renter_constants
from ratings import ratings_to_csv

def main(argv):
  opts, args = getopt.getopt(argv, 'f:m', ['fake-prices', 'multiple-files'])

  use_fake_prices = False
  use_multiple_files = False
  for opt, arg in opts:
    if opt in ('-f', '--fake-price'):
      use_fake_prices = True
    elif opt in ('-m', '--multiple-files'):
      use_multiple_files = True

  if not use_fake_prices:
    print("NOT GENERATE FAKE PRICES")

  if use_multiple_files:
    print("GENERATE MULTIPLE FILES")

  w = ratings_to_csv.RequestWriter(
    renter_constants, use_multiple_files=use_multiple_files, use_fake_prices=use_fake_prices)
  w.write()

if __name__ == '__main__':
  main(sys.argv[1:])
