import numpy as np

def IsReportSafe(report):
  """Determines if a report is safe

  A report (list of ints) is safe if all numbers are either increasing
  or decreasing (not both) and the difference between any two consecutive
  numbers is between 1 and 3 inclusive

  Parameters
    ----------
    report: np.array(int)
        The report to check

    Returns
    -------
    bool
        Whether the report is safe or not
  """
  differences = np.diff(report)
  return np.all((abs(differences) > 0) & (abs(differences) < 4)) and (np.all(differences > 0) or np.all(differences < 0))

test_cases = [
    np.array([7, 6, 4, 2, 1]),
    np.array([1, 2, 7, 8, 9]),
    np.array([9, 7, 6, 2, 1]),
    np.array([1, 3, 2, 4, 5]),
    np.array([8, 6, 4, 4, 1]),
    np.array([1, 3, 6, 7, 9])
]
test_cases_safety = [True, False, False, False, False, True]

def TestIsReportSafe():
  assert IsReportSafe(np.array([0])) == True
  assert IsReportSafe(np.array([1])) == True
  assert IsReportSafe(np.array([1, 2])) == True
  assert IsReportSafe(np.array([1, 4])) == True
  assert IsReportSafe(np.array([2, 1])) == True
  assert IsReportSafe(np.array([4, 1])) == True
  assert IsReportSafe(np.array([4, 3, 2, 1])) == True
  assert IsReportSafe(np.array([1, 3, 6, 7, 9, 10])) == True
  assert IsReportSafe(np.array([1, 5])) == False
  assert IsReportSafe(np.array([5, 1])) == False
  assert IsReportSafe(np.array([1, 1])) == False
  assert IsReportSafe(np.array([1, 2, 1])) == False
  assert IsReportSafe(np.array([2, 1, 2])) == False
  for test_case, test_case_safety in zip(test_cases, test_cases_safety):
    assert IsReportSafe(test_case) == test_case_safety

def IsDampenedReportSafe(report):
  """Determines if a dampened report is safe

  A dampened report (list of ints) is safe if the report itself is safe
  (using `IsReportSafe`) or if the report is safe after removing any
  single element

  Parameters
    ----------
    report: np.array(int)
        The report to check

    Returns
    -------
    bool
        Whether the report is safe or not
  """
  return IsReportSafe(report) or np.any([IsReportSafe(np.delete(report, i)) for i in range(report.shape[0])])

test_cases_dampened_safety = [True, False, False, True, True, True]

def TestIsDampenedReportSafe():
  assert IsDampenedReportSafe(np.array([0])) == True
  assert IsDampenedReportSafe(np.array([1])) == True
  assert IsDampenedReportSafe(np.array([1, 2])) == True
  assert IsDampenedReportSafe(np.array([1, 4])) == True
  assert IsDampenedReportSafe(np.array([2, 1])) == True
  assert IsDampenedReportSafe(np.array([4, 1])) == True
  assert IsDampenedReportSafe(np.array([4, 3, 2, 1])) == True
  assert IsDampenedReportSafe(np.array([1, 3, 6, 7, 9, 10])) == True
  assert IsDampenedReportSafe(np.array([1, 5])) == True
  assert IsDampenedReportSafe(np.array([5, 1])) == True
  assert IsDampenedReportSafe(np.array([1, 1])) == True
  assert IsDampenedReportSafe(np.array([1, 2, 1])) == True
  assert IsDampenedReportSafe(np.array([2, 1, 2])) == True
  assert IsDampenedReportSafe(np.array([1, 5, 9])) == False
  assert IsDampenedReportSafe(np.array([2, 1, 1, 2])) == False
  for test_case, test_case_safety in zip(test_cases, test_cases_dampened_safety):
    assert IsDampenedReportSafe(test_case) == test_case_safety
