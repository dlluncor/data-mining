"""
  Logs to SETI generates SETI from the logged information (renters CSV).
"""
import renter_form

def _to_renter_form(csv_line):
  return renter_form.RenterForm()

def generate_seti(filenames):
  # TODO(haoran): Convert CSV lines to RenterForm.
  setis = []
  # Read each file where each row represents a training example.
  for fname in filenames:
    # Read examples from file.
    csv_lines = open(fname, 'r')
    for csv_line in csv_lines:
      renter_form = _to_renter_form(csv_line)
      fe = FeatureExtractor()
      seti = fe.to_seti(renter_form)
      setis.append(seti)
  return setis
