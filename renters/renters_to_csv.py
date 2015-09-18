import renter_constants
import ratings.ratings_to_csv

def main():
  w = ratings_to_csv.RequestWriter(renter_constants, multiple_files=False)
  w.write()

main()