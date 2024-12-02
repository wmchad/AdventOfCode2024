import numpy as np
import os
os.system('pip install pytest')

def ListDistance(list_a, list_b):
    """Gets the distance between two lists by pairing up entries and taking the difference

    Compares the values ordinally (sorted) and sums the absolute difference between entries

    Parameters
    ----------
    list_a: np.array[int]
        The first list to compare
    list_b: np.array[int]
        The second list to compare

    Returns
    -------
    int
        The total difference between the two lists
    """
    return sum([abs(a - b) for a, b in zip(sorted(list_a), sorted(list_b))])

test_case = {
    "a": np.array([3, 4, 2, 1, 3, 3]),
    "b": np.array([4, 3, 5, 3, 9, 3])
}
test_case_distance = 11

def TestListDistance():
    assert ListDistance(np.array([0]), np.array([0])) == 0
    assert ListDistance(np.array([0]), np.array([5])) == 5
    assert ListDistance(np.array([3, 1]), np.array([2, 6])) == 4
    assert ListDistance(np.array([3, 1]), np.array([2, 2,])) == 2
    assert ListDistance(test_case['a'], test_case['b']) == test_case_distance

def ListSimilarityScore(list_a, list_b):
    """Gets the similarity score between two lists

    For each number in list_a, sum that number times the number of times it appears in list_b

    Parameters
    ----------
    list_a: np.array[int]
        The first list to compare
    list_b: np.array[int]
        The second list to compare

    Returns
    -------
    int
        The similarity score between the two lists
    """
    return sum([a * np.count_nonzero(list_b == a) for a in list_a])

test_case_similarity_score = 31

def TestListSimilarityScore():
    assert ListSimilarityScore(np.array([0]), np.array([0])) == 0
    assert ListSimilarityScore(np.array([5]), np.array([5])) == 5
    assert ListSimilarityScore(np.array([5]), np.array([4])) == 0
    assert ListSimilarityScore(np.array([3, 1]), np.array([2, 6])) == 0
    assert ListSimilarityScore(np.array([1, 2, 3, 2]), np.array([5, 2, 2, 6])) == 8
    assert ListSimilarityScore(test_case['a'], test_case['b']) == test_case_similarity_score
    