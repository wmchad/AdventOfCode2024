def ParseCalibrationLine(cal_line):
  """parses a calibration equation line

  The line has the form `<X>: <Y1> <Y2> ...`

  Parameters
  ----------
  cal_line: str
    The calibration equation

  Returns
  -------
  dict
    A dictionary with the following entries:
    * target (int): the target number for the equation
    * factors (list[int]): the numbers to use to hit the target
  
  """
  pieces = cal_line.split()
  return {"target": int(pieces[0][:-1]), "factors": list(map(int, pieces[1:]))}
  
def ParseCalibrationData(input_string):
  """parses a set of calibration equations

  Parameters
  ----------
  input_string: str
    The calibration equations as a single string separated by newlines

  Returns
  -------
  list[dict]
    A list of calibration equations, parsed by `ParseCalibrationLine()`
  
  """
  return [ParseCalibrationLine(x) for x in input_string.strip().split('\n')]

def IsTargetCalculable(target, factors):
  """determines whether a target can be achieved using the given factors

  The factors are evaluated left to right and
  can be combined via addition or multiplication

  Parameters
  ----------
  target: int
    The target number for the equation
  factors: list[int]
    The factors to use to get to the target

  Returns
  -------
  bool
    Whether the target can be calculated from the given factors
  
  """
  if len(factors) == 1:
    return target == factors[0]
  else:
    return IsTargetCalculable(target, [factors[0] + factors[1]] + factors[2:]) \
      or IsTargetCalculable(target, [factors[0] * factors[1]] + factors[2:])

def IsTargetCalculableWithConcatenation(target, factors):
  """determines whether a target can be achieved using the given factors

  The factors are evaluated left to right and
  can be combined via addition, multiplication, or string concatenation

  Parameters
  ----------
  target: int
    The target number for the equation
  factors: list[int]
    The factors to use to get to the target

  Returns
  -------
  bool
    Whether the target can be calculated from the given factors
  
  """
  if len(factors) == 1:
    return target == factors[0]
  else:
    return IsTargetCalculableWithConcatenation(target, [factors[0] + factors[1]] + factors[2:]) \
      or IsTargetCalculableWithConcatenation(target, [factors[0] * factors[1]] + factors[2:]) \
      or IsTargetCalculableWithConcatenation(target, [int(str(factors[0]) + str(factors[1]))] + factors[2:])

test_input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

test_parsed_data = [
  {"target": 190,    "factors": [10, 19]},
  {"target": 3267,   "factors": [81, 40, 27]},
  {"target": 83,     "factors": [17, 5]},
  {"target": 156,    "factors": [15, 6]},
  {"target": 7290,   "factors": [6, 8, 6, 15]},
  {"target": 161011, "factors": [16, 10, 13]},
  {"target": 192,    "factors": [17, 8, 14]},
  {"target": 21037,  "factors": [9, 7, 18, 13]},
  {"target": 292,    "factors": [11, 6, 16, 20]},
]

test_is_calculable                    = [True, True, False, False, False, False, False, False, True]
test_is_calculable_with_concatenation = [True, True, False, True, True, False, True, False, True]

def TestParseCalibrationLine():
  parsed_data = ParseCalibrationLine("7290: 6 8 6 15")
  assert parsed_data["target"]  == 7290
  assert parsed_data["factors"] == [6, 8, 6, 15]
  print("ParseCalibrationLine() passed testing.")

def TestParseCalibrationData():
  assert ParseCalibrationData(test_input) == test_parsed_data
  print("ParseCalibrationData() passed testing.")

def TestIsTargetCalculable():
  assert [IsTargetCalculable(x["target"], x["factors"]) for x in test_parsed_data] == test_is_calculable
  print("IsTargetCalculable() passed testing.")

def TestIsTargetCalculableWithConcatenation():
  assert [IsTargetCalculableWithConcatenation(x["target"], x["factors"]) for x in test_parsed_data] == test_is_calculable_with_concatenation
  print("IsTargetCalculableWithConcatenation() passed testing.")