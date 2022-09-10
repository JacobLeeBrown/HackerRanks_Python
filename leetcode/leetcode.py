
from typing import List, Optional
from ListNode import ListNode
from Nodes import Node, TreeNode

my_list = ["1", 2, "three"]
# Set
my_set = {"1", 2, "three"}
# Map / Dict
my_map = {"1": 1, "two": 2, "tres": 3}
my_map2 = {'a': [0, 1, 2], 'c': [2, 1, 0], 'b': [1, 2, 3]}


class Solution:

    def __init__(self):
        self.first_bad_version = 0  # 278 element
        self.fib_nums = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]  # 509 element
        self.steps_nums = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]  # 70 element

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

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 206
        if head is None:
            return head
        last_node = None
        cur_node = head
        next_node = cur_node.next
        while next_node is not None:
            cur_node.next = last_node
            last_node = cur_node
            cur_node = next_node
            next_node = cur_node.next
        cur_node.next = last_node
        return cur_node

    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 876
        i = 1
        mid_node = head
        cur_node = head
        while cur_node is not None:
            if i % 2 == 0:
                mid_node = mid_node.next
                i = 0
            cur_node = cur_node.next
            i += 1
        return mid_node

    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 142
        # Only faster than 20% of submissions, and only uses less memory than 10% of submissions
        # TODO: Improve time and/or space complexity, try for O(1) space
        if head is None or head.next is None:
            return None

        id_map = {id(head): head}
        while head is not None:
            head = head.next
            if id(head) in id_map:
                return id_map[id(head)]
            id_map[id(head)] = head
        return None

    def maxProfit(self, prices: List[int]) -> int:
        # 121
        if len(prices) <= 1:
            return 0
        relative_min = prices[0]
        best_profit = 0
        for price in prices:
            pot_profit = price - relative_min
            if pot_profit > best_profit:
                best_profit = pot_profit
            elif price < relative_min:
                relative_min = price
        return best_profit

    def longestPalindrome(self, s: str) -> int:
        # 409
        if len(s) <= 1:
            return len(s)
        char_count = {}
        for char in s:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1
        have_odd = False
        palindrome_length = 0
        for key in char_count:
            count = char_count[key]
            if count % 2 == 0:
                palindrome_length += count
            elif not have_odd:
                palindrome_length += count
                have_odd = True
            else:
                palindrome_length += (count - 1)
        return palindrome_length

    def preorder(self, root: Node) -> List[int]:
        # 589
        # TODO: setup testing framework and unit tests
        if root is None:
            return []

        sub_preorder = [root.val]
        for child in root.children:
            sub_preorder += self.preorder(child)
        return sub_preorder

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # 102
        # Only faster than 20% of submissions, and only uses less memory than 10% of submissions
        # TODO: Improve time and/or space complexity
        return self.level_order_helper(root, [], 0)

    def level_order_helper(self, root: Optional[TreeNode], res: List[List[int]], level: int) -> List[List[int]]:
        if root is None:
            return res
        if level >= len(res):
            res.append([root.val])
        else:
            res[level].append(root.val)

        res = self.level_order_helper(root.left, res, level + 1)
        return self.level_order_helper(root.right, res, level + 1)

    def binary_search(self, nums: List[int], target: int) -> int:
        # 704
        # Super slow (only beats 5%), but space efficient (better than 73%)
        # TODO: Speed up
        return self.binary_search_helper(nums, target, 0)

    def binary_search_helper(self, nums: List[int], target: int, start_idx: int) -> int:
        nums_len = len(nums)
        if nums_len == 0:
            return -1
        elif nums_len == 1:
            if nums[0] == target:
                return start_idx
            else:
                return -1

        mid_idx = int(nums_len/2)
        mid_val = nums[mid_idx]
        if target == mid_val:
            return start_idx+mid_idx
        elif target > mid_val:
            return self.binary_search_helper(nums[mid_idx+1:], target, start_idx+mid_idx+1)
        else:
            return self.binary_search_helper(nums[:mid_idx], target, start_idx)

    def firstBadVersion(self, n: int) -> int:
        # 278
        return self.first_bad_version_helper(1, n)

    def first_bad_version_helper(self, start: int, end: int) -> int:
        # 278 helper
        if start == end:
            return start
        mid_version = start + int((end-start)/2)
        if self.isBadVersion(mid_version):
            return self.first_bad_version_helper(start, mid_version)
        else:
            return self.first_bad_version_helper(mid_version+1, end)

    def isBadVersion(self, n: int) -> bool:
        # 278 element
        return n >= self.first_bad_version

    def set_first_bad_version(self, n: int) -> None:
        # 278 element
        self.first_bad_version = n

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # 98
        return self.is_valid_bst_helper(root, None, None)

    def is_valid_bst_helper(self, root: Optional[TreeNode], min_val: Optional[int], max_val: Optional[int]) -> bool:
        # 98 helper
        if root is None:
            return True
        elif (min_val is not None and root.val <= min_val) \
                or (max_val is not None and root.val >= max_val):
            return False
        else:
            return self.is_valid_bst_helper(root.left, min_val, root.val) \
                   and self.is_valid_bst_helper(root.right, root.val, max_val)

    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        # 235
        # Tree is a Binary Search Tree
        # The number of nodes in the tree is in the range [2, 10^5].
        # -10^9 <= Node.val <= 10^9
        # All Node.val are unique.
        # p != q
        # p and q will exist in the BST.
        p_val = p.val
        q_val = q.val
        if p_val < q_val:
            return self.lowest_common_ancestor_helper(root, p_val, q_val)
        else:
            return self.lowest_common_ancestor_helper(root, q_val, p_val)

    def lowest_common_ancestor_helper(self, root: TreeNode, p_val: int, q_val: int) -> TreeNode:
        # 235 helper
        # Assumes p_val < q_val
        cur_val = root.val
        if cur_val == p_val or cur_val == q_val or (p_val < cur_val < q_val):
            return root
        elif cur_val < p_val:
            return self.lowest_common_ancestor_helper(root.right, p_val, q_val)
        else:  # cur_val > q_val
            return self.lowest_common_ancestor_helper(root.left, p_val, q_val)

    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        # 733
        if image[sr][sc] == color:
            return image
        m = len(image)
        n = len(image[0])
        visited = [[False for _ in range(n)] for _ in range(m)]
        self.flood_fill_helper(image, visited, m, n, image[sr][sc], color, sr, sc)
        return image

    def flood_fill_helper(self, image: List[List[int]], visited: List[List[bool]],
                          m: int, n: int, old_color: int, new_color: int, r: int, c: int) -> None:
        # 733 helper
        if m <= r or r < 0 or n <= c or c < 0 or visited[r][c] or image[r][c] != old_color:
            return

        visited[r][c] = True
        image[r][c] = new_color
        self.flood_fill_helper(image, visited, m, n, old_color, new_color, r, c+1)
        self.flood_fill_helper(image, visited, m, n, old_color, new_color, r, c-1)
        self.flood_fill_helper(image, visited, m, n, old_color, new_color, r+1, c)
        self.flood_fill_helper(image, visited, m, n, old_color, new_color, r-1, c)

    def numIslands(self, grid: List[List[str]]) -> int:
        # 200
        # Super slow (only beats 5%), but space efficient (better than 82%)
        m = len(grid)
        n = len(grid[0])
        visited = [[False for _ in range(n)] for _ in range(m)]
        island_count = 0
        for row in range(m):
            for col in range(n):
                if not visited[row][col] and grid[row][col] == '1':
                    island_count += 1
                    self.num_islands_helper(grid, visited, m, n, row, col)
        return island_count

    def num_islands_helper(self, grid: List[List[str]], visited: List[List[bool]],
                           m: int, n: int, row: int, col: int):
        # 200 helper
        # Will mark all spaces of an island as visited
        if row < 0 or col < 0 or row >= m or col >= n or visited[row][col] or grid[row][col] == '0':
            return

        visited[row][col] = True
        self.num_islands_helper(grid, visited, m, n, row+1, col)
        self.num_islands_helper(grid, visited, m, n, row-1, col)
        self.num_islands_helper(grid, visited, m, n, row, col+1)
        self.num_islands_helper(grid, visited, m, n, row, col-1)

    def fib(self, n: int) -> int:
        # 509
        fib_limit = len(self.fib_nums)
        while fib_limit <= n:
            fn_2 = self.fib_nums[fib_limit-2]
            fn_1 = self.fib_nums[fib_limit-1]
            self.fib_nums.append(fn_2 + fn_1)
            fib_limit += 1
        return self.fib_nums[n]

    def climbStairs(self, n: int) -> int:
        # 70 original
        # Only faster than 10%, less memory than 57%
        steps_limit = len(self.steps_nums)
        while steps_limit <= n:
            fn_2 = self.steps_nums[steps_limit-2]
            fn_1 = self.steps_nums[steps_limit-1]
            self.steps_nums.append(fn_2 + fn_1)
            steps_limit += 1
        return self.steps_nums[n]

    def climbStairs_alt1(self, n: int) -> int:
        # 70 alternate 1
        # Faster than 90%, only less memory than 12%
        steps_nums = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144,
                      233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946,
                      17711, 28657, 46368, 75025, 121393, 196418, 317811,
                      514229, 832040, 1346269, 2178309, 3524578, 5702887,
                      9227465, 14930352, 24157817, 39088169, 63245986,
                      102334155, 165580141, 267914296, 433494437,
                      701408733, 1134903170, 1836311903, 2971215073]
        return steps_nums[n]

    def climbStairs_alt2(self, n: int) -> int:
        # 70 alternate 2
        # Faster than 99%, less memory usage than 57%! Best of the 3 versions
        steps_nums = [0, 1, 2]
        steps_limit = len(steps_nums)
        while steps_limit <= n:
            fn_2 = steps_nums[steps_limit-2]
            fn_1 = steps_nums[steps_limit-1]
            steps_nums.append(fn_2 + fn_1)
            steps_limit += 1
        return steps_nums[n]

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # 746
        # Took a while to reason through, but faster than 98% and less memory than 74%!!!
        if len(cost) < 2:
            return 0
        mins = [cost[0], cost[1]]
        costs = len(cost)
        for i in range(2, costs):
            min2 = mins[i-2]
            min1 = mins[i-1]
            best_min = min1 if min1 <= min2 else min2
            cur_min = cost[i] + best_min
            mins.append(cur_min)
        return mins[costs-2] if mins[costs-2] <= mins[costs-1] else mins[costs-1]

    def uniquePaths(self, m: int, n: int) -> int:
        # 62
        # Solution grid is:
        # 1  1  1  1  1  ...
        # 1  2  3  4  5  ...
        # 1  3  6  10 15 ...
        # 1  4  10 20 35 ...
        # 1  5  15 35 70 ...
        # Only faster than 15%, less memory than 75%

        if m < 1 or n < 1:
            return 0
        sol_grid = [[1 for _ in range(n)] for _ in range(m)]
        for i in range(1, m):
            for j in range(1, n):
                sol_grid[i][j] = sol_grid[i-1][j] + sol_grid[i][j-1]
        return sol_grid[m-1][n-1]

    def findAnagrams(self, s: str, p: str) -> List[int]:
        # 438
        # TODO: I don't wanna think through this right now, will do later
        return [0]

if __name__ == '__main__':
    sol = Solution()
