import renter_constants
import ratings.ratings_to_csv

def main():
  # TODO(dlluncor): Fill in the CSV files with a fake price information
  # and save to a CSV file.
  w = ratings_to_csv.RequestWriter(renter_constants, multiple_files=False)
  w.write()

main()