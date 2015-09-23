"""
  Feature extractor generates the features given an input vector.
"""

from ml import seti

class FeatureExtractor(object):
  def __init__(self, for_test=False):
    self.for_test = for_test

  def to_seti(self, rf):
    """
    Args:
      rf: A renter_form.RenterForm.
    """
    # Do all logic to produce a SETI example here.
    s = seti.SETIExample()
    s.add_continuous('dob', rf.get_age())
    s.add_binary('gender', rf.gender)
    s.weight = 1
    s.label = rf.label
    if self.for_test:
      return s
    s.add_continuous('deductible', rf.get_deductible())
    s.add_continuous('personal_property_value', rf.personal_property_value)
    s.add_continuous('personal_liability', rf.personal_liability)
    return s


