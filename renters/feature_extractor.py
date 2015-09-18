"""
  Feature extractor generates the features given an input vector.
"""

from ml import seti
class FeatureExtractor(object):
  def __init__(self):
    pass

  def to_seti(self, renter_form):
    """
    Args:
      renter_form: A renter_form.RenterForm.
    """
    # Do all logic to produce a SETI example here.
    s = seti.SETIExample()
    s.add_continuous('dob', renter_form.get_age())
    s.add_binary('gender', renter_form.gender)
    s.weight = 1
    s.label = renter_form.label
    return s


