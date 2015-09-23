
import logs_to_seti
from ml import seti

def testLogsToSeti():
  # First three lines are copied from tdg_v0.csv
  csvs = ['testdata/logs_to_seti_csv0.csv']
  # s0. dob: 05/06/1989. gender:f
  # s1. dob: 05/06/1949. gender:m
  s0 = seti.create_seti(19.15, bfs=[('gender', 'f')], cfs=[('dob', 26.0)])
  s1 = seti.create_seti(22.51, bfs=[('gender', 'm')], cfs=[('dob', 66.0)])

  # Test model gets created and loaded.
  # Test that we can score one example.
  setis = logs_to_seti.generate_seti(csvs)
  wants = [s0, s1]
  for i in xrange(len(setis)):
    assertEquals(str(wants[i]), str(setis[i]))

def testToRenterForm():
  csv_line = 'Renters,95111,Gideon,Garrett,6/6/1986,f,2600 Corde Terra Cir,San Jose,CA,N,RENTED HOUSE - SINGLE FAMILY,1,0,0,(415) 552-9443,owen.lloyd@foxmail.com,N,N,N,N,Y,N,NONE,N,N,Keep default.,4000,Keep default,1000,100000,N,100 / 250,90961327,93,$245.70,Diem Pham,"1900 Camden Ave San Jose CA 95124-2942 (408) 9007200"'
  line = csv_line.split(',')
  r, _ = logs_to_seti._to_renter_form(line)
  assertFloatEquals(245.7, r.label)

# Test util template.
import sys
import inspect

errs = []

def assertFloatEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  v0 = '%.4f' % expected
  v1 = '%.4f' % got
  if v0 != v1:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

def assertEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  if expected != got:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

def main():
  funs = dir(sys.modules[__name__])
  for fun in funs:
    if fun.startswith('test'):
      globals()[fun]()
  if len(errs) == 0:
    print '%s test passes!' % (sys.argv[0])
  else:
    for err in errs:
      print err
  
if __name__ == '__main__':
  main()