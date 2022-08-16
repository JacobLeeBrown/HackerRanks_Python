
# List
from typing import List

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
            print(f'sum_ltor = {sum_ltor}, sum_rtol = {sum_rtol}')
        print(running_sums_ltor)
        print(running_sums_rtol)

        for i, num in enumerate(running_sums_ltor):
            if num == running_sums_rtol[i]:
                return i
        return -1


if __name__ == '__main__':
    sol = Solution()
    print(sol.pivotIndex([2, 1, -1]))
