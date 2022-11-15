# import packages
import unittest
import compute_stats2

# reminder: when running in command line type: python3 -m unittest test_compute_stats2

class TestComputeStats(unittest.TestCase):

    # testing list with an even number of elements
    def test_even_number_list(self):
        list = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
        results = compute_stats2.compute_stats(list)
        # using assertAlmostEqual for floats
        self.assertAlmostEqual(results, (1.1, 1.6, 1.35, 1.35))

    # testing list with an odd number of elements
    def test_odd_number_list(self):
        list = [2.1 , 2.2, 2.3, 2.4, 2.5]
        results = compute_stats2.compute_stats(list)
        # using assertAlmostEqual for floats
        self.assertAlmostEqual(results, (2.1, 2.5, 2.3, 2.3))

    # testing an empty list
    def test_empty_list(self):
        list = []
        results = compute_stats2.compute_stats(list)
        self.assertIsNone(results)

    # testing a list with only one element
    def test_single_element_list(self):
        list = [1.1]
        results = compute_stats2.compute_stats(list)
        self.assertAlmostEqual(results, (1.1, 1.1, 1.1, 1.1))

    # testing a list of strings
    def test_string_list(self):
        with self.assertRaises(TypeError):
            # should get a TypeError on the mean() call of the function
            list = ["Paul", "George", "John", "Ringo"]
            compute_stats2.compute_stats(list)
