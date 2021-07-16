import unittest
import longest_substring


class TestLongestSubstring(unittest.TestCase):

    def test_empty_string_returns_zero(self):
        test_str = ""
        expected = 0

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

    def test_one_char_returns_one(self):
        test_str = "1"
        expected = 1

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

    def test_no_repeats_returns_length(self):
        test_str = "abcdefghij"
        expected = 10

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

    def test_repeats_at_bounds(self):
        test_str = "1234561111"
        expected = 6

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

        test_str = "0004567890"
        expected = 7

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

    def test_interwoven_repeats(self):
        test_str = "1234561121"
        expected = 6

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

        test_str = "0004564890"
        expected = 6

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

    def test_only_repeats_returns_one(self):
        test_str = "9999999999"
        expected = 1

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

        test_str = "jjjjjjjjjj"
        expected = 1

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

    def test_tied_best_substrings(self):
        test_str = "1234123"
        expected = 4

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)

        test_str = "111a2b3c4d1a22"
        expected = 8

        actual = longest_substring.longest_substring(test_str)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
