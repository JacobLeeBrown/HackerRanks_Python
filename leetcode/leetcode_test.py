import unittest
from typing import List, Optional
from leetcode import Solution
import ListNode as ln

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

    def _assertEqualLinkedList(self, list1: List[int], list2: Optional[ln.ListNode]):
        list2_ = ln.to_list(list2)
        self.assertEqual(list1, list2_)

    def test_merge_two_lists(self):
        self._assertEqualLinkedList([], sol.mergeTwoLists(None, None))
        self._assertEqualLinkedList([1, 2], sol.mergeTwoLists(None, ln.from_list([1, 2])))
        self._assertEqualLinkedList([1, 2], sol.mergeTwoLists(ln.from_list([1, 2]), None))
        self._assertEqualLinkedList(
            [1, 1, 2, 2],
            sol.mergeTwoLists(
                ln.from_list([1, 2]),
                ln.from_list([1, 2]))
        )
        self._assertEqualLinkedList(
            [1, 1, 1, 2, 2, 3, 5, 5, 6, 9],
            sol.mergeTwoLists(
                ln.from_list([1, 1, 2, 5, 6, 9]),
                ln.from_list([1, 2, 3, 5]))
        )
        self._assertEqualLinkedList(
            [-1, 0, 0, 1, 2, 4],
            sol.mergeTwoLists(
                ln.from_list([1, 2]),
                ln.from_list([-1, 0, 0, 4]))
        )


if __name__ == '__main__':
    unittest.main()