
from typing import List, Optional
from ListNode import ListNode

my_list = ["1", 2, "three"]
# Set
my_set = {"1", 2, "three"}
# Map / Dict
my_map = {"1": 1, "two": 2, "tres": 3}
my_map2 = {'a': [0, 1, 2], 'c': [2, 1, 0], 'b': [1, 2, 3]}


class Solution:

    def runningSum(self, nums: List[int]) -> List[int]:
        # 1480
        running_sum = 0
        for i, num in enumerate(nums):
            running_sum += num
            nums[i] = running_sum
        return nums

    def pivotIndex(self, nums: List[int]) -> int:
        # 724
        size = len(nums)
        running_sums_ltor = [0]*size
        running_sums_rtol = [0]*size
        sum_ltor = 0
        sum_rtol = 0
        for i, num in enumerate(nums):
            running_sums_ltor[i] = sum_ltor
            running_sums_rtol[size-(i+1)] = sum_rtol
            sum_ltor += num
            sum_rtol += nums[size-(i+1)]

        for i, num in enumerate(running_sums_ltor):
            if num == running_sums_rtol[i]:
                return i
        return -1

    def isIsomorphic(self, s: str, t: str) -> bool:
        # 205
        i = 0
        d_s = {}
        d_t = {}
        for char_s in s:
            char_t = t[i]
            if char_s not in d_s:
                if char_t in d_t:
                    return False
                d_s[char_s] = char_t
                d_t[char_t] = char_s
            else:
                if d_s[char_s] != char_t or char_t not in d_t or d_t[char_t] != char_s:
                    return False
            i += 1
        return True

    def isSubsequence(self, s: str, t: str) -> bool:
        # 392
        if len(s) == 0:
            return True
        elif len(t) == 0:
            return False
        i = 0
        cur_char_s = s[i]
        for char_t in t:
            if char_t == cur_char_s:
                i += 1
                if i == len(s):
                    return True
                cur_char_s = s[i]
        return False

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # 21
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        if list1.val <= list2.val:
            head = list1
            moving_head = list1
            list1 = list1.next
        else:
            head = list2
            moving_head = list2
            list2 = list2.next

        while True:
            if list1 is None:
                moving_head.next = list2
                return head
            elif list2 is None:
                moving_head.next = list1
                return head
            elif list1.val <= list2.val:
                moving_head.next = list1
                moving_head = list1
                list1 = list1.next
            else:
                moving_head.next = list2
                moving_head = list2
                list2 = list2.next


if __name__ == '__main__':
    sol = Solution()
    print(sol.pivotIndex([2, 1, -1]))
