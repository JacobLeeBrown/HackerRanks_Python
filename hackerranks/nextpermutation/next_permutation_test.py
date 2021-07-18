import unittest
from next_permutation import next_permutation


class MyTestCase(unittest.TestCase):

    def test_least_permutation(self):
        actual = [1, 2, 3]

        # Should not have to reassign since operation is in-place
        next_permutation(actual)

        expected = [1, 3, 2]

        self.assertEqual(expected, actual)

    def test_multiple_calls_on_same_list(self):
        actual = [1, 2, 3]

        next_permutation(actual)  # [1, 3, 2]
        next_permutation(actual)  # [2, 1, 3]
        next_permutation(actual)  # [2, 3, 1]

        expected = [2, 3, 1]

        self.assertEqual(expected, actual)

    def test_empty_list_unchanged(self):
        actual = []
        expected = []

        next_permutation(actual)

        self.assertEqual(expected, actual)

    def test_singleton_list_unchanged(self):
        actual = [123]
        expected = [123]

        next_permutation(actual)

        self.assertEqual(expected, actual)

    def test_greatest_permutation_returns_least_permutation(self):
        actual = [3, 2, 1]

        next_permutation(actual)

        expected = [1, 2, 3]

        self.assertEqual(expected, actual)

    def test_unordered_list(self):
        actual = [5, 3, 7, 6, 4]

        next_permutation(actual)

        expected = [5, 4, 3, 6, 7]

        self.assertEqual(expected, actual)

    def test_duplicates(self):
        actual = [4, 3, 4, 6, 4]

        next_permutation(actual)

        expected = [4, 3, 6, 4, 4]

        self.assertEqual(expected, actual)

    def test_many_duplicates(self):
        actual = [4, 6, 6, 4, 4]

        next_permutation(actual)

        expected = [6, 4, 4, 4, 6]

        self.assertEqual(expected, actual)

    def test_only_duplicates_unchanged(self):
        actual = [1, 1, 1, 1]

        next_permutation(actual)

        expected = [1, 1, 1, 1]

        self.assertEqual(expected, actual)

    def test_multi_digit_elems(self):
        actual = [20, 21, 32, 55, 1000, 117, 99]

        next_permutation(actual)

        expected = [20, 21, 32, 99, 55, 117, 1000]

        self.assertEqual(expected, actual)

    def test_with_zeros(self):
        actual = [4, 0, 4, 3, 1, 0]

        next_permutation(actual)

        expected = [4, 1, 0, 0, 3, 4]

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
