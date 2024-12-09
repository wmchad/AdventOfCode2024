import numpy as np

def IsStringInDirection(search_string, word_search, start, direction):
  """tests to see if a string is in a word search at the particular place and direction

  Parameters
  ----------
  search_string: str
    The string to search for
  word_search: np.chararry
    The 2-d array of characters making up the word search
  start: tuple(int)
    The start position to look for the search string (2 element indices for the word_search)
  direction: tuple(int)
    The direction to look for the search string (2 elements, each must be -1, 0, or 1)

  Returns
  -------
  bool
    Whether the search string is in the word search or not
  """
  next_start = (start[0] + direction[0], start[1] + direction[1])
  found_string = False
  if len(search_string) == 0:
    found_string = True
  elif word_search[start] == search_string[0]:
    if len(search_string) == 1:
      found_string = True
    if all([x >= 0 for x in next_start]) and next_start[0] < word_search.shape[0] and next_start[1] < word_search.shape[1]:
      return IsStringInDirection(search_string[1:], word_search, next_start, direction)
  return found_string

def CountXmas(word_search):
  """counts all occurences of 'XMAS' in the given word search

  Parameters
  ----------
  word_search: np.chararry
    The 2-d array of characters making up the word search

  Returns
  -------
  int
    The number of times 'XMAS' appears in any direction
  """
  return sum([IsStringInDirection('XMAS', word_search, (i, j), (d1, d2))
              for i in range(word_search.shape[0])
              for j in range(word_search.shape[1])
              for d1 in [-1, 0, 1]
              for d2 in [-1, 0, 1]
             ])

test_case = np.char.array(list(
  "MMMSXXMASMMSAMXMSMSAAMXSXMAAMMMSAMASMSMXXMASAMXAMMXXAMMXXAMASMSMSASXSSSAXAMASAAAMAMMMXMMMMMXMXAXMASX"
)).reshape(10, 10)
test_case_count = 18

def TestCountXmas():
  assert CountXmas(test_case) == test_case_count

def IsMasX(word_search, start):
  return word_search[start] == 'A' and \
  set([word_search[start[0] - 1, start[1] - 1], word_search[start[0] + 1, start[1] + 1]]) == set(['M', 'S']) and \
  set([word_search[start[0] - 1, start[1] + 1], word_search[start[0] + 1, start[1] - 1]]) == set(['M', 'S'])

def CountMasX(word_search):
  """counts all occurences of X patterns of 'MAS' in the given word search

  Parameters
  ----------
  word_search: np.chararry
    The 2-d array of characters making up the word search

  Returns
  -------
  int
    The number of times X patterns of 'MAS' appears in any direction
  """
  return sum([IsMasX(word_search, (i, j))
              for i in range(1, word_search.shape[0] - 1)
              for j in range(1, word_search.shape[1] - 1)
             ])

test_case_mas_x = 9

def TestCountMasX():
  assert CountMasX(test_case) == test_case_mas_x