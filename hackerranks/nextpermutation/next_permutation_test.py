import unittest
from next_permutation import next_permutation


class MyTestCase(unittest.TestCase):

    def test_happy_path(self):
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

    def test_empty_list_remains_empty(self):
        actual = []
        expected = []

        next_permutation(actual)

        self.assertEqual(expected, actual)

    def test_singleton_list_unchanged(self):
        actual = [123]
        expected = [123]

        next_permutation(actual)

        self.assertEqual(expected, actual)

    def test_list_in_greatest_permutation_returns_least_permutation(self):
        actual = [3, 2, 1]

        next_permutation(actual)

        expected = [1, 2, 3]

        self.assertEqual(expected, actual)

    def test_list_with_duplicates(self):
        actual = [4, 3, 4, 6, 4]

        next_permutation(actual)

        expected = [4, 3, 6, 4, 4]

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
