import unittest
from typing import List, Optional
from leetcode import Solution
import ListNode as Ln
import Nodes as N

sol = Solution()


class TestLeetCode(unittest.TestCase):

    def test_running_sum(self):
        self.assertEqual([], sol.runningSum([]))
        self.assertEqual([-1], sol.runningSum([-1]))
        self.assertEqual([4, 3, 10], sol.runningSum([4, -1, 7]))

    def test_pivot_index(self):
        self.assertEqual(-1, sol.pivotIndex([]))
        self.assertEqual(1, sol.pivotIndex([1, 2, 1]))
        self.assertEqual(0, sol.pivotIndex([1, 2, -2]))
        self.assertEqual(2, sol.pivotIndex([-2, 2, 1]))
        self.assertEqual(-1, sol.pivotIndex([1, 2, 3, 4, 5]))
        self.assertEqual(2, sol.pivotIndex([1, 2, 3, 4, -1]))

    def test_is_isomorphic(self):
        self.assertEqual(True, sol.isIsomorphic('a', 'b'))
        self.assertEqual(False, sol.isIsomorphic('ab', 'cc'))
        self.assertEqual(True, sol.isIsomorphic('egg', 'add'))
        self.assertEqual(True, sol.isIsomorphic('@#$@', 'test'))

    def test_is_subsequence(self):
        self.assertEqual(True, sol.isSubsequence('', ''))
        self.assertEqual(True, sol.isSubsequence('', 'asdf'))
        self.assertEqual(False, sol.isSubsequence('asdf', ''))
        self.assertEqual(True, sol.isSubsequence('asdf', 'asdf'))
        self.assertEqual(False, sol.isSubsequence('a', 'bcdef'))
        self.assertEqual(False, sol.isSubsequence('aa', 'asdf'))
        self.assertEqual(True, sol.isSubsequence('aa', 'asda'))
        self.assertEqual(False, sol.isSubsequence('aabc', 'asbcda'))
        self.assertEqual(True, sol.isSubsequence('aabc', 'asbcdabca'))

    def _assertEqualLinkedList(self, list1: List[int], list2: Optional[Ln.ListNode], limit=-1):
        list2_ = Ln.to_list(list2, limit)
        self.assertEqual(list1, list2_)

    def test_merge_two_lists(self):
        self._assertEqualLinkedList([], sol.mergeTwoLists(None, None))
        self._assertEqualLinkedList([1, 2], sol.mergeTwoLists(None, Ln.from_list([1, 2])))
        self._assertEqualLinkedList([1, 2], sol.mergeTwoLists(Ln.from_list([1, 2]), None))
        self._assertEqualLinkedList(
            [1, 1, 2, 2],
            sol.mergeTwoLists(
                Ln.from_list([1, 2]),
                Ln.from_list([1, 2]))
        )
        self._assertEqualLinkedList(
            [1, 1, 1, 2, 2, 3, 5, 5, 6, 9],
            sol.mergeTwoLists(
                Ln.from_list([1, 1, 2, 5, 6, 9]),
                Ln.from_list([1, 2, 3, 5]))
        )
        self._assertEqualLinkedList(
            [-1, 0, 0, 1, 2, 4],
            sol.mergeTwoLists(
                Ln.from_list([1, 2]),
                Ln.from_list([-1, 0, 0, 4]))
        )

    def test_reverse_list(self):
        self._assertEqualLinkedList([], sol.reverseList(None))
        self._assertEqualLinkedList([1], sol.reverseList(Ln.from_list([1])))
        self._assertEqualLinkedList([1, 1], sol.reverseList(Ln.from_list([1, 1])))
        self._assertEqualLinkedList([3, 2, 1], sol.reverseList(Ln.from_list([1, 2, 3])))

    def test_middle_node(self):
        self._assertEqualLinkedList([], sol.middleNode(None))
        self._assertEqualLinkedList([1], sol.middleNode(Ln.from_list([1])))
        self._assertEqualLinkedList([2], sol.middleNode(Ln.from_list([1, 2])))
        self._assertEqualLinkedList([2, 3], sol.middleNode(Ln.from_list([1, 2, 3])))
        self._assertEqualLinkedList([4, 5, 6], sol.middleNode(Ln.from_list([1, 2, 3, 4, 5, 6])))

    def test_detect_cycle(self):
        self._assertEqualLinkedList([], sol.detectCycle(None))
        self._assertEqualLinkedList([], sol.detectCycle(Ln.from_list_and_tail_pointer([1], -1)), 1)
        self._assertEqualLinkedList([1], sol.detectCycle(Ln.from_list_and_tail_pointer([1], 0)), 1)
        self._assertEqualLinkedList([], sol.detectCycle(Ln.from_list_and_tail_pointer([1, 1, 1], -1)))
        self._assertEqualLinkedList([1, 1], sol.detectCycle(Ln.from_list_and_tail_pointer([1, 1, 1], 1)), 2)
        self._assertEqualLinkedList([3], sol.detectCycle(Ln.from_list_and_tail_pointer([-1, 0, 5, 3], 3)), 1)
        self._assertEqualLinkedList([-1, 0, 5, 3], sol.detectCycle(Ln.from_list_and_tail_pointer([-1, 0, 5, 3], 0)), 4)
        self._assertEqualLinkedList([5, 3], sol.detectCycle(Ln.from_list_and_tail_pointer([-1, 0, 5, 3], 2)), 2)

    def test_max_profit(self):
        self.assertEqual(0, sol.maxProfit([]))
        self.assertEqual(0, sol.maxProfit([1]))
        self.assertEqual(0, sol.maxProfit([3, 2, 1]))
        self.assertEqual(6, sol.maxProfit([3, 2, 1, 7]))
        self.assertEqual(9, sol.maxProfit([3, 2, 1, 7, 0, 9]))

    def test_longest_palindrome(self):
        self.assertEqual(0, sol.longestPalindrome(''))
        self.assertEqual(1, sol.longestPalindrome('a'))
        self.assertEqual(1, sol.longestPalindrome('abcdef'))
        self.assertEqual(1, sol.longestPalindrome('aA'))
        self.assertEqual(8, sol.longestPalindrome('abcdabcd'))
        self.assertEqual(9, sol.longestPalindrome('abcdeabcd'))

    def test_level_order(self):
        self.assertEqual([], sol.levelOrder(N.tnodes_from_array([])))
        self.assertEqual([[1]], sol.levelOrder(N.tnodes_from_array([[1]])))
        self.assertEqual([[0], [1, 2], [3, 4, 5, 6]],
                         sol.levelOrder(N.tnodes_from_array([[0], [1, 2], [3, 4], [5, 6]])))
        self.assertEqual([[0], [1, 2], [3, 4, 5, 6]],
                         sol.levelOrder(N.tnodes_from_array([[0], [1, 2], [3, 4], [5, 6]])))
        self.assertEqual([[0], [1], [3, 4], [7]],
                         sol.levelOrder(N.tnodes_from_array([[0], [1, None], [3, 4], [None, None], [None, 7]])))

    def test_binary_search(self):
        self.assertEqual(-1, sol.binary_search([], 5))
        self.assertEqual(0, sol.binary_search([5], 5))
        self.assertEqual(2, sol.binary_search([-5, -3, 0, 2, 4], 0))
        self.assertEqual(2, sol.binary_search([0, 1, 2, 3, 4], 2))
        self.assertEqual(1, sol.binary_search([0, 1, 2, 3, 4], 1))
        self.assertEqual(0, sol.binary_search([0, 1, 2, 3, 4], 0))
        self.assertEqual(3, sol.binary_search([0, 1, 2, 3, 4], 3))
        self.assertEqual(-1, sol.binary_search([0, 1, 2, 3], -5))
        self.assertEqual(-1, sol.binary_search([0, 1, 2, 3], 5))
        self.assertEqual(4, sol.binary_search([-1, 0, 3, 5, 9, 12], 9))

    def test_first_bad_version(self):
        sol.set_first_bad_version(1)
        self.assertEqual(1, sol.firstBadVersion(1))
        self.assertEqual(1, sol.firstBadVersion(2))
        self.assertEqual(1, sol.firstBadVersion(4))

        sol.set_first_bad_version(4)
        self.assertEqual(4, sol.firstBadVersion(4))
        self.assertEqual(4, sol.firstBadVersion(8))
        self.assertEqual(4, sol.firstBadVersion(128))

    def test_is_valid_bst(self):
        self.assertEqual(True, sol.isValidBST(N.tnodes_from_array([])))
        self.assertEqual(True, sol.isValidBST(N.tnodes_from_array([[1]])))
        self.assertEqual(False, sol.isValidBST(N.tnodes_from_array([[0], [1, 2], [3, 4], [5, 6]])))
        self.assertEqual(True, sol.isValidBST(N.tnodes_from_array([[0], [-5, 5], [-6, -4], [4, 6]])))
        self.assertEqual(True, sol.isValidBST(N.tnodes_from_array([[0], [None, 5], [None, None], [None, 6]])))
        self.assertEqual(True, sol.isValidBST(N.tnodes_from_array([[0], [-5, None], [-6, None], [None, None]])))
        self.assertEqual(False, sol.isValidBST(N.tnodes_from_array([[0], [-5, None], [-6, 1], [None, None]])))

    def test_lowest_common_ancestor_helper(self):
        self.assertEqual(1, sol.lowest_common_ancestor_helper(
            N.tnodes_from_array([[1], [None, 3]]), 1, 3).val)
        self.assertEqual(0, sol.lowest_common_ancestor_helper(
            N.tnodes_from_array([[0], [-5, 3]]), -5, 3).val)
        self.assertEqual(5, sol.lowest_common_ancestor_helper(
            N.tnodes_from_array([[0], [-5, 5], [-7, -3], [3, 7]]), 3, 7).val)
        self.assertEqual(0, sol.lowest_common_ancestor_helper(
            N.tnodes_from_array([[0], [-5, 5], [-7, -3], [3, 7]]), -5, 3).val)
        self.assertEqual(0, sol.lowest_common_ancestor_helper(
            N.tnodes_from_array([[0], [-5, 5], [-7, -3], [3, 7]]), 0, -7).val)
        self.assertEqual(-5, sol.lowest_common_ancestor_helper(
            N.tnodes_from_array([[0], [-5, 5], [-7, -3], [3, 7]]), -5, -3).val)

    def test_flood_fill(self):
        image = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        expec = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(expec, sol.floodFill(image, 1, 1, 0))
        image = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        expec = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        self.assertEqual(expec, sol.floodFill(image, 1, 1, 1))
        image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
        expec = [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
        self.assertEqual(expec, sol.floodFill(image, 2, 0, 2))
        image = [[1, 1, 1], [1, 1, 0], [1, 0, 1], [1, 0, 1]]
        expec = [[1, 1, 1], [1, 1, 0], [1, 2, 1], [1, 2, 1]]
        self.assertEqual(expec, sol.floodFill(image, 2, 1, 2))

    def test_num_islands(self):
        islands = [
            ['1', '1', '1'],
            ['1', '1', '1'],
            ['1', '1', '1']
        ]
        self.assertEqual(1, sol.numIslands(islands))
        islands = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]
        self.assertEqual(0, sol.numIslands(islands))
        islands = [
            ['1', '1', '1'],
            ['1', '0', '1'],
            ['1', '1', '1']
        ]
        self.assertEqual(1, sol.numIslands(islands))
        islands = [
            ['1', '0', '1'],
            ['0', '0', '0'],
            ['1', '0', '1']
        ]
        self.assertEqual(4, sol.numIslands(islands))

    def test_fib(self):
        self.assertEqual(0, sol.fib(0))
        self.assertEqual(1, sol.fib(1))
        self.assertEqual(1, sol.fib(2))
        self.assertEqual(89, sol.fib(11))
        self.assertEqual(4181, sol.fib(19))

    def test_climb_stairs(self):
        self._test_climb_stairs(sol.climbStairs)
        self._test_climb_stairs(sol.climbStairs_alt1)
        self._test_climb_stairs(sol.climbStairs_alt2)

    def _test_climb_stairs(self, climb_stairs_method):
        self.assertEqual(0, climb_stairs_method(0))
        self.assertEqual(1, climb_stairs_method(1))
        self.assertEqual(2, climb_stairs_method(2))
        self.assertEqual(89, climb_stairs_method(10))
        self.assertEqual(4181, climb_stairs_method(18))

    def test_min_cost_climbing_stairs(self):
        self.assertEqual(0, sol.minCostClimbingStairs([]))
        self.assertEqual(0, sol.minCostClimbingStairs([20]))
        self.assertEqual(10, sol.minCostClimbingStairs([10, 20]))
        self.assertEqual(5, sol.minCostClimbingStairs([10, 5]))
        self.assertEqual(5, sol.minCostClimbingStairs([10, 5, 12]))
        self.assertEqual(17, sol.minCostClimbingStairs([10, 5, 12, 20]))
        self.assertEqual(22, sol.minCostClimbingStairs([10, 15, 12, 20]))

    def test_unique_paths(self):
        self.assertEqual(0, sol.uniquePaths(0, 0))
        self.assertEqual(0, sol.uniquePaths(0, 6))
        self.assertEqual(0, sol.uniquePaths(4, 0))
        self.assertEqual(1, sol.uniquePaths(1, 1))
        self.assertEqual(1, sol.uniquePaths(1, 6))
        self.assertEqual(1, sol.uniquePaths(4, 1))
        self.assertEqual(10, sol.uniquePaths(3, 4))
        self.assertEqual(10, sol.uniquePaths(4, 3))
        self.assertEqual(70, sol.uniquePaths(5, 5))

    def test_find_anagrams(self):
        self.assertEqual([], sol.findAnagrams('a', 'b'))
        self.assertEqual([0], sol.findAnagrams('a', 'a'))
        self.assertEqual([0, 2], sol.findAnagrams('abcba', 'abc'))
        self.assertEqual([3], sol.findAnagrams('abdcba', 'abc'))
        self.assertEqual([0], sol.findAnagrams('abcdba', 'abc'))
        self.assertEqual([0, 1, 2, 3], sol.findAnagrams('abcabc', 'abc'))
        self.assertEqual([1, 2, 3, 5], sol.findAnagrams('abacbabc', 'abc'))

    def test_character_replacement(self):
        self.assertEqual(1, sol.characterReplacement('A', 0))
        self.assertEqual(1, sol.characterReplacement('A', 1))
        self.assertEqual(1, sol.characterReplacement('A', 2))
        self.assertEqual(2, sol.characterReplacement('AA', 1))
        self.assertEqual(2, sol.characterReplacement('AB', 1))
        self.assertEqual(4, sol.characterReplacement('AABABBA', 1))
        self.assertEqual(2, sol.characterReplacement('ABAA', 0))
        self.assertEqual(4, sol.characterReplacement('ABBB', 2))

    def test_num_binary_ones(self):
        self.assertEqual(0, sol._num_binary_ones(0))
        self.assertEqual(1, sol._num_binary_ones(1))
        self.assertEqual(1, sol._num_binary_ones(2))
        self.assertEqual(2, sol._num_binary_ones(3))
        self.assertEqual(1, sol._num_binary_ones(4))
        self.assertEqual(2, sol._num_binary_ones(5))
        self.assertEqual(2, sol._num_binary_ones(6))

    def test_count_bits(self):
        self.assertEqual([0], sol.countBits_old(0))
        self.assertEqual([0, 1], sol.countBits_old(1))
        self.assertEqual([0, 1, 1], sol.countBits_old(2))
        self.assertEqual([0, 1, 1, 2], sol.countBits_old(3))
        self.assertEqual([0, 1, 1, 2, 1], sol.countBits_old(4))
        self.assertEqual([0, 1, 1, 2, 1, 2], sol.countBits_old(5))
        self.assertEqual([0, 1, 1, 2, 1, 2, 2], sol.countBits_old(6))

    def test_count_bits(self):
        self.assertEqual([0], sol.countBits(0))
        self.assertEqual([0, 1], sol.countBits(1))
        self.assertEqual([0, 1, 1], sol.countBits(2))
        self.assertEqual([0, 1, 1, 2], sol.countBits(3))
        self.assertEqual([0, 1, 1, 2, 1], sol.countBits(4))
        self.assertEqual([0, 1, 1, 2, 1, 2], sol.countBits(5))
        self.assertEqual([0, 1, 1, 2, 1, 2, 2], sol.countBits(6))

    def test_is_divisor_of(self):
        self.assertEqual(True, sol._isDivisorOf('ab', 'ababab'))
        self.assertEqual(True, sol._isDivisorOf('ab', 'ab'))
        self.assertEqual(False, sol._isDivisorOf('a', 'ab'))
        self.assertEqual(False, sol._isDivisorOf('c', 'ab'))
        self.assertEqual(False, sol._isDivisorOf('ab', 'abababc'))
        self.assertEqual(False, sol._isDivisorOf('abcdefg', 'ab'))
        self.assertEqual(False, sol._isDivisorOf('ababab', 'ab'))

    def test_gcd_of_strings(self):
        self.assertEqual('ab', sol.gcdOfStrings('ab', 'ababab'))
        self.assertEqual('ab', sol.gcdOfStrings('abab', 'ababab'))
        self.assertEqual('', sol.gcdOfStrings('abc', 'ababab'))
        self.assertEqual('', sol.gcdOfStrings('abab', 'abcabcabc'))
        self.assertEqual('', sol.gcdOfStrings('', 'abcabcabc'))
        self.assertEqual('', sol.gcdOfStrings('ab', ''))

    def test_kids_with_candies(self):
        self.assertEqual([False, False, True], sol.kidsWithCandies([1, 1, 6], 3))
        self.assertEqual([True, False, True], sol.kidsWithCandies([3, 1, 6], 3))
        self.assertEqual([True, True, True], sol.kidsWithCandies([3, 1, 6], 5))

    def test_max_area(self):
        self.assertEqual(1, sol.maxArea([1, 1]))
        self.assertEqual(49, sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))
        self.assertEqual(4, sol.maxArea([1, 2, 3, 2, 1]))
        self.assertEqual(9, sol.maxArea([1, 2, 3, 4, 5, 6]))
        self.assertEqual(24, sol.maxArea([1, 3, 2, 5, 25, 24, 5]))

    def test_find_max_average(self):
        self.assertAlmostEqual(1, sol.findMaxAverage([1, 1, 1, 1, 1], 3))
        self.assertAlmostEqual(2, sol.findMaxAverage([1, 2, 2, 2, 1], 3))
        self.assertAlmostEqual(5, sol.findMaxAverage([5], 1))
        self.assertAlmostEqual(5, sol.findMaxAverage([10, 0, 5, 5, 5], 3))
        self.assertAlmostEqual(5, sol.findMaxAverage([10, 0, 5, 5, 5], 5))
        self.assertAlmostEqual(6, sol.findMaxAverage([5, 0, 3, 6, -4, -1], 1))

    def test_pair_sum(self):
        self.assertEqual(4, sol.pairSum(Ln.from_list([3, 1])))
        self.assertEqual(4, sol.pairSum(Ln.from_list([3, 1, 3, 1])))
        self.assertEqual(7, sol.pairSum(Ln.from_list([3, 2, 5, 0])))
        self.assertEqual(3, sol.pairSum(Ln.from_list([3, -2, 5, 0])))
        self.assertEqual(0, sol.pairSum(Ln.from_list([3, -2, 1, -3])))

    def test_can_place_flowers(self):
        self.assertEqual(True, sol.canPlaceFlowers([], 0))
        self.assertEqual(False, sol.canPlaceFlowers([], 1))
        self.assertEqual(True, sol.canPlaceFlowers([1], 0))
        self.assertEqual(False, sol.canPlaceFlowers([1], 1))
        self.assertEqual(True, sol.canPlaceFlowers([0], 1))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0], 1))
        self.assertEqual(False, sol.canPlaceFlowers([0, 0], 2))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 0], 1))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 0], 2))
        self.assertEqual(False, sol.canPlaceFlowers([0, 1, 0], 1))
        self.assertEqual(True, sol.canPlaceFlowers([1, 0, 0], 1))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 1], 1))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 0, 0, 0], 3))
        self.assertEqual(False, sol.canPlaceFlowers([0, 1, 0, 0, 0], 2))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 1, 0, 0], 2))
        self.assertEqual(False, sol.canPlaceFlowers([0, 0, 1, 0, 0, 1], 2))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 1, 0, 1, 0], 1))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 1, 0, 0, 0, 1, 0], 2))
        self.assertEqual(False, sol.canPlaceFlowers([1, 0, 0, 0, 0, 1], 2))
        self.assertEqual(True, sol.canPlaceFlowers([0, 0, 0, 0, 1], 2))

    def test_find_difference(self):
        self.assertEqual([[1, 3], [4, 6]], sol.findDifference([1, 2, 3], [2, 4, 6]))
        self.assertEqual([[1, 2, 3], []], sol.findDifference([1, 2, 3], []))
        self.assertEqual([[], [2, 4, 6]], sol.findDifference([], [2, 4, 6]))
        self.assertEqual([[], [2, 4]], sol.findDifference([1, 3, 3], [1, 1, 2, 3, 4]))

    def test_min_flips(self):
        self.assertEqual(0, sol.minFlips(4, 2, 6))
        self.assertEqual(0, sol.minFlips(4, 0, 4))
        self.assertEqual(0, sol.minFlips(4, 4, 4))
        self.assertEqual(1, sol.minFlips(4, 2, 7))
        self.assertEqual(4, sol.minFlips(6, 3, 0))
        self.assertEqual(2, sol.minFlips(12, 3, 3))
        self.assertEqual(4, sol.minFlips(0, 0, 15))

    def test_nearest_exit(self):
        self.assertEqual(2, sol.nearestExit(
            [
                ['+', '+', '+'],
                ['.', '.', '.'],
                ['+', '+', '+']
            ],
            [1, 0]
        ))
        self.assertEqual(1, sol.nearestExit(
            [
                ['+', '+', '+'],
                ['.', '.', '.'],
                ['+', '+', '+']
            ],
            [1, 1]
        ))
        self.assertEqual(-1, sol.nearestExit(
            [
                ['+', '+', '+'],
                ['+', '.', '+'],
                ['+', '+', '+']
            ],
            [1, 1]
        ))
        self.assertEqual(2, sol.nearestExit(
            [
                ['+', '.', '+'],
                ['+', '.', '+'],
                ['+', '.', '+']
            ],
            [0, 1]
        ))


if __name__ == '__main__':
    unittest.main()
