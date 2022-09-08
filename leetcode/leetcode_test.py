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

if __name__ == '__main__':
    unittest.main()
