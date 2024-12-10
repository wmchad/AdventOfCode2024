import numpy as np

def BuildMap(map_string):
  """builds a map grid from an input string

  Parameters
  ----------
  map_string: str
    The input data as a single string with newlines

  Returns
  -------
  np.array[str]
    A 2-dimensional array representing the map.
    * '.' is an empty space
    * '#' is an obstacle
    * '<', '^', '>', and 'v' represent the guard and the direction he is facing
  
  """
  return np.array([list(x) for x in map_string.strip().split()])

def FindStartPositionAndDirection(input_map):
  """finds the starting position and direction of the guard in a map

  Parameters
  ----------
  input_map: np.array[str]
    The map to search

  Returns
  -------
  (np.array[int], np.array[int])
    a tuple with two entries
    * the current position of the guard
    * the direction the guard is facing
  
  """
  # The four directions and associated movement vectors
  directions = {
    "<": np.array([0, -1]),
    "^": np.array([-1, 0]),
    ">": np.array([0, 1]),
    "v": np.array([1, 0])
  }
  
  cur_direction = np.array([0, 0])
  cur_position  = (-1, -1)

  # Find the starting location and direction
  for d in directions.keys():
    found_location = np.argwhere(input_map == d)
    if len(found_location) > 0:
      cur_direction = directions[d]
      cur_position  = found_location[0]
  return (cur_position, cur_direction)

def NumberOfDistinctPositions(input_map):
  """gets the number of distinct positions the guard visits in a map before leaving the mapped area

  The guard always moves in a straight line until meeting an obstacle, which causes him to turn right

  Parameters
  ----------
  input_map: np.array[str]
    The map of the area, including guard starting position

  Returns
  -------
  int
    The number of places on the map the guard visits before leaving
  
  """
  # The rotation matrix for changing direction
  rotation_matrix = np.array([[0, -1], [1, 0]])

  cur_position, cur_direction = FindStartPositionAndDirection(input_map)
  visited_positions = set()
  while cur_position[0] in range(len(input_map)) and \
        cur_position[1] in range(len(input_map[0])):
    if input_map[tuple(cur_position)] == '#': # Found a roadblock - back up and change direction
      cur_position -= cur_direction
      cur_direction = np.matmul(cur_direction, rotation_matrix)
    else:
      visited_positions.add(tuple(cur_position))
      cur_position += cur_direction
  return len(visited_positions)

def ObstacleCausesLoop(input_map, obstacle_position):
  """determines whether placing an obstacle at a given position in a map will cause
  the guard to enter a looping pattern. Cannot place an obstacle on the guard start position.

  Parameters
  ----------
  input_map: np.array[str]
    The map of the area, including guard starting position
  obstacle_position: (int, int)
    The position to place a new obstacle to see if the guard enters a loop

  Returns
  -------
  bool
    Whether the guard gets stuck in a loop
  
  """
  new_map = input_map.copy()
  new_map[obstacle_position] = '#'
  # The rotation matrix for changing direction
  rotation_matrix = np.array([[0, -1], [1, 0]])

  cur_position, cur_direction = FindStartPositionAndDirection(new_map)
  if tuple(cur_position) == obstacle_position:
    return False
  visited_positions = set()
  while cur_position[0] in range(len(new_map)) and \
        cur_position[1] in range(len(new_map[0])):
    if (tuple(cur_position), tuple(cur_direction)) in visited_positions:
      return True
    elif new_map[tuple(cur_position)] == '#': # Found a roadblock - back up and change direction
      cur_position -= cur_direction
      cur_direction = np.matmul(cur_direction, rotation_matrix)
    else:
      visited_positions.add((tuple(cur_position), tuple(cur_direction)))
      cur_position += cur_direction
  return False

def ObstacleLoopPositions(input_map):
  """gets the set of positions on a map that will cause the guard to enter a loop

  Parameters
  ----------
  input_map: np.array[str]
    The map of the area, including guard starting position

  Returns
  -------
  set[(int, int)]
    The set of positions for a new obstacle that will cause the guard to go into a loop
  
  """
  cur_position, cur_direction = FindStartPositionAndDirection(input_map)
  return {x for x in np.ndindex(input_map.shape) if ObstacleCausesLoop(input_map, x)}
  
test_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

test_map = np.array([
  ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '#', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '#', '.', '.', '^', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
  ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.']
])

test_n_positions = 41

test_loop_positions = {(6, 3), (7, 6), (7, 7), (8, 1), (8, 3), (9, 7)}

def TestBuildMap():
  assert np.array_equal(BuildMap(test_input), test_map)

def TestNumberOfDistinctPositions():
  assert NumberOfDistinctPositions(test_map) == test_n_positions

def TestObstacleCausesLoop():
  for obs_pos in test_loop_positions:
    assert ObstacleCausesLoop(test_map, obs_pos)
  assert ~ObstacleCausesLoop(test_map, (6, 2))
  assert ~ObstacleCausesLoop(test_map, (6, 4))

def TestObstacleLoopPositions():
  assert ObstacleLoopPositions(test_map) == test_loop_positions