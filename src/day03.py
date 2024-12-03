import numpy as np
import re

def FindAndCalculateMuls(memory):
  """Finds and computes all mul instructions in a memory string

  mul instructions have the form `mul(X,Y)`. This function finds all valid
  instructions and returns the results of the multiplications (`X*Y`) in an array.

  Parameters
    ----------
    memory: string
        The memory string to check

    Returns
    -------
    np.array(int)
        The list of computed mul instructions
  """
  valid_mul_re = r'mul\((?P<X>\d+),(?P<Y>\d+)\)'
  return np.array([int(x) * int(y) for [x, y] in re.findall(valid_mul_re, memory)])

test_case      = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
test_case_muls = np.array([8, 25, 88, 40])

def TestFindAndCalculateMuls():
  assert np.array_equal(FindAndCalculateMuls(test_case), test_case_muls)

def FindAndCalculateMulsWithCmds(memory, include_mul = True):
  """Finds and computes all mul instructions in a memory string,
     modified by `do()` and `don't()` commands

  Similar to `FindAndCalculateMuls`, but this time `don't()` commands turn off muls
  and `do()` commands turn on muls. muls on at beginning.

  Parameters
    ----------
    memory: string
        The memory string to check

    Returns
    -------
    np.array(int)
        The list of computed mul instructions
  """
  valid_mul_cmd_re = r'(?P<mul>mul\((?P<X>\d+),(?P<Y>\d+)\))|(?P<do>do\(\))|(?P<dont>don\'t\(\))'
  matches = re.findall(valid_mul_cmd_re, memory)
  muls = []
  for match in matches:
    if match[3] == 'do()':
      include_mul = True
    elif match[4] == "don't()":
      include_mul = False
    elif include_mul:
      muls.append(int(match[1]) * int(match[2]))
  return [np.array(muls), include_mul]

test_case_with_cmds        = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
test_case_with_cmds_muls_t = np.array([8, 40])
test_case_with_cmds_muls_f = np.array([40])

def TestFindAndCalculateMulsWithCmds():
  assert np.array_equal(FindAndCalculateMulsWithCmds(test_case_with_cmds, True)[0], test_case_with_cmds_muls_t)
  assert np.array_equal(FindAndCalculateMulsWithCmds(test_case_with_cmds, False)[0], test_case_with_cmds_muls_f)
