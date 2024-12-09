def ProcessInputData(input_data):
  """processes input data into rules and print queues

  Parameters
  ----------
  input_data: str
    The input data as a single string with newlines

  Returns
  -------
  dict
    A dictionary with 'rules' and 'queues', each containing a list of lists of ints
    representing the parsed rules and queues
  
  """
  input_lines = input_data.strip().split()
  # Iterates through the list twice, maybe not the most efficient
  rules = [list(map(int, x.split("|"))) for x in input_lines if "|" in x]
  print_queues = [list(map(int, x.split(","))) for x in input_lines if "|" not in x]
  return {"rules": rules, "queues": print_queues}

def QueuePassesRules(queue, rules):
  """determines whether a print queue satisfies all the rules

  The rules are of the form [p1, p2], indicating that if both p1 and p2
  are in the print queue, then p1 must come before p2

  Parameters
  ----------
  queue: list[int]
    The print queue as a list of pages to be printed
  rules: list[list[int]]
    The rules that need to be satisfied

  Returns
  -------
  bool
    Whether or not the print queue satisfies all the rules
  
  """
  # Check all ordered pairs in the queue
  # Return False if an ordered pair exists in the rules in the opposite direction
  # Otherwise return True
  for i in range(len(queue) - 1):
    for j in queue[(i + 1):]:
        if [j, queue[i]] in rules:
          return False
  return True

def GetMiddlePageNumbersOfPassingQueues(queues, rules):
  """gets the middle page numbers of all queues that pass the rules

  Parameters
  ----------
  queue: list[list[int]]
    The list of print queues, each as a list of pages to be printed
  rules: list[list[int]]
    The rules that need to be satisfied

  Returns
  -------
  list[int]
    The list of middle page numbers for passing queues
  
  """
  return [queue[(len(queue) - 1) // 2] for queue in queues if QueuePassesRules(queue, rules)]

def CorrectedQueue(queue, rules):
  """fixes the page numbers in a queue so it follows all the rules

  Parameters
  ----------
  queue: list[int]
    The print queue as a list of pages to be printed
  rules: list[list[int]]
    The rules that need to be satisfied

  Returns
  -------
  list[int]
    The corrected print queue
  
  """
  for i in range(len(queue) - 1):
    for j in range(i + 1, len(queue)):
        if [queue[j], queue[i]] in rules:
          corrected_queue = queue.copy()
          corrected_queue[i], corrected_queue[j] = corrected_queue[j], corrected_queue[i]
          return CorrectedQueue(corrected_queue, rules)
  return queue

test_data = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

parsed_test_data = {
  "rules": [
    [47, 53], [97, 13], [97, 61], [97, 47], [75, 29], [61, 13], [75, 53],
    [29, 13], [97, 29], [53, 29], [61, 53], [97, 53], [61, 29], [47, 13],
    [75, 47], [97, 75], [47, 61], [75, 61], [47, 29], [75, 13], [53, 13]
  ],
  "queues": [
    [75, 47, 61, 53, 29],
    [97, 61, 53, 29, 13],
    [75, 29, 13],
    [75, 97, 47, 61, 53],
    [61, 13, 29],
    [97, 13, 75, 29, 47]
  ]
}

test_queues_passing = [True, True, True, False, False, False]

expected_middle_pages = [61, 53, 29]

corrected_test_queues = [
    [75, 47, 61, 53, 29],
    [97, 61, 53, 29, 13],
    [75, 29, 13],
    [97, 75, 47, 61, 53],
    [61, 29, 13],
    [97, 75, 47, 29, 13]
  ]

def TestProcessInputData():
  assert ProcessInputData(test_data) == parsed_test_data

def TestQueuePassesRules():
  for queue, expected_result in zip(parsed_test_data["queues"], test_queues_passing):
    assert QueuePassesRules(queue, parsed_test_data["rules"]) == expected_result

def TestGetMiddlePageNumbersOfPassingQueues():
  assert GetMiddlePageNumbersOfPassingQueues(parsed_test_data["queues"], parsed_test_data["rules"]) == expected_middle_pages

def TestCorrectedQueue():
  for queue, expected_result in zip(parsed_test_data["queues"], corrected_test_queues):
    assert CorrectedQueue(queue, parsed_test_data["rules"]) == expected_result
