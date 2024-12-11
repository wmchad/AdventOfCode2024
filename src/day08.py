import itertools
import numpy as np

def ParseAntennaMapString(input_string):
  """parses a string representing a map of antenna positions

  Parameters
  ----------
  input_string: str
    The map as a single string separated by newlines

  Returns
  -------
  dict
    A dictionary with the following elements:
    * positions: a dictionary of sets of antenna positions, grouped by antenna type
    * map_size: a tuple indicating the size of the map
  
  """
  antenna_map = input_string.strip().split('\n')
  antenna_dict = {}
  for i, map_line in enumerate(antenna_map):
      for j, loc_str in enumerate(map_line):
          if loc_str != '.':
              if loc_str in antenna_dict:
                  antenna_dict[loc_str].add((i, j))
              else:
                  antenna_dict[loc_str] = {(i, j)}
  return {
    "positions": antenna_dict,
    "map_size": (len(antenna_map), len(antenna_map[0]))
  }

def GetAntinodeLocations(antenna_map):
  """gets a list of antinode locations for a parsed map

  Parameters
  ----------
  antenna_map: dict
    The parsed map from `ParseAntennaMapString()`

  Returns
  -------
  set[tuple]
    A set of locations for all antinodes
  
  """
  res_locs = set()
  for antenna_set in antenna_map["positions"].values():
    for loc1, loc2 in list(itertools.combinations(antenna_set, 2)):
      loc1 = np.array(loc1)
      loc2 = np.array(loc2)
      diff = loc1 - loc2
      res_locs.add(tuple(loc1 + diff))
      res_locs.add(tuple(loc2 - diff))
  return {x for x in res_locs if \
          x[0] in range(antenna_map["map_size"][0]) and \
          x[1] in range(antenna_map["map_size"][1])}

def GetAntinodeLocationsWithResonantHarmonics(antenna_map):
  """gets a list of antinode locations for a parsed map when including resonant harmonics

  Parameters
  ----------
  antenna_map: dict
    The parsed map from `ParseAntennaMapString()`

  Returns
  -------
  set[tuple]
    A set of locations for all antinodes
  
  """
  res_locs = set()
  for antenna_set in antenna_map["positions"].values():
    for loc1, loc2 in list(itertools.combinations(antenna_set, 2)):
      res_locs.add(loc1)
      res_locs.add(loc2)
      loc1 = np.array(loc1)
      loc2 = np.array(loc2)
      diff = loc1 - loc2
      next_loc = loc1 + diff
      while next_loc[0] in range(antenna_map["map_size"][0]) and \
            next_loc[1] in range(antenna_map["map_size"][1]):
        res_locs.add(tuple(next_loc))
        next_loc += diff
      next_loc = loc1 - diff
      while next_loc[0] in range(antenna_map["map_size"][0]) and \
            next_loc[1] in range(antenna_map["map_size"][1]):
        res_locs.add(tuple(next_loc))
        next_loc -= diff
  return res_locs

        


#-------------------------------------------------------------------#
#------------------------------Testing------------------------------#
#-------------------------------------------------------------------#

test_input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

test_antenna_locations = {
  '0': {(1, 8), (2, 5), (3, 7), (4, 4)},
  'A': {(5, 6), (8, 8), (9, 9)}
}

test_map_size = (12, 12)

test_parsed_map = {
  "positions": test_antenna_locations,
  "map_size": test_map_size
}

test_resonant_locations = {
  (0, 6), (0, 11), (1, 3), (2, 4), (2, 10), (3, 2), (4, 9),
  (5, 1), (5, 6), (6, 3), (7, 0), (7, 7), (10, 10), (11, 10)
}

test_n_resonant_harmonics_locations = 34

def TestParseAntennaMapString():
  assert ParseAntennaMapString(test_input) == test_parsed_map
  print("ParseAntennaMapString() passed testing.")

def TestGetAntinodeLocations():
  assert GetAntinodeLocations(test_parsed_map) == test_resonant_locations
  print("GetAntinodeLocations() passed testing.")

def TestGetAntinodeLocationsWithResonantHarmonics():
  assert len(GetAntinodeLocationsWithResonantHarmonics(test_parsed_map)) == test_n_resonant_harmonics_locations
  print("GetAntinodeLocationsWithResonantHarmonics() passed testing.")