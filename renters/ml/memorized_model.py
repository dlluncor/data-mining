
import seti, csv

class Memorizer(object):
  
  def __init__(self):
    pass

  def write_features(self, tdg_blocks, filename):
    """
    Args:
      tdg_blocks: An array of training_data.TDGBlock to write for memorization.
    """
    with open(filename, 'wb') as fin:
      writer = csv.writer(fin)
      for tdg_block in tdg_blocks:
        seti_model_key = seti.standard_repr(tdg_block.feature_vector)
        row = (seti_model_key, tdg_block.label)
        writer.writerow(row)
    print 'Wrote memorized features to: %s' % (filename)

  def read_features(self, filename):
    prices = {}
    with open(filename, 'rb') as fin:
        reader = csv.reader(fin)
        for key, price in reader:
            prices[key] = price
    return prices