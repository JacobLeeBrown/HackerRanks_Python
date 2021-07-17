import unittest
from my_atoi import my_atoi


class TestLongestSubstring(unittest.TestCase):

    def test_normal_positive_int(self):
        s = "1234"
        self.assertEqual(1234, my_atoi(s))

    def test_ignores_leading_spaces(self):
        s = "       1234"
        self.assertEqual(1234, my_atoi(s))

    def test_reads_signs(self):
        s = "+1234"
        self.assertEqual(1234, my_atoi(s))

        s = "-1234"
        self.assertEqual(-1234, my_atoi(s))

    def test_ignores_everything_after_first_non_digit(self):
        s = "1234 5678 9000"
        self.assertEqual(1234, my_atoi(s))

        s = "1234asdf1234"
        self.assertEqual(1234, my_atoi(s))

    def test_valid_zero_strings(self):
        s = "0"
        self.assertEqual(0, my_atoi(s))

        s = "    -0000"
        self.assertEqual(0, my_atoi(s))

        s = "    +0000zyxw"
        self.assertEqual(0, my_atoi(s))

    def test_zero_edge_cases(self):
        s = ""
        self.assertEqual(0, my_atoi(s))

        s = "   +"
        self.assertEqual(0, my_atoi(s))

        s = "   -asdf"
        self.assertEqual(0, my_atoi(s))

    def test_32_bit_signed_bounds(self):
        s = "2147483648"  # 2**31 = upper_bound + 1 -> should return 2**31-1
        self.assertEqual(2147483647, my_atoi(s))

        s = "-2147483649"  # -2**31-1 = lower_bound - 1 -> should return -2**31
        self.assertEqual(-2147483648, my_atoi(s))


if __name__ == '__main__':
    unittest.main()
