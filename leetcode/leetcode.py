
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
        # Example
        #   Input: s = "cbaebabacd", p = "abc"
        #   Output: [0,6]
        # Only faster than 16%, and only less memory than 6%
        # TODO: Improve significantly

        p_len = len(p)
        p_map = {}
        for p_char in p:
            if p_char not in p_map:
                p_map[p_char] = 1
            else:
                p_map[p_char] += 1

        window_start = -1  # -1 means no current moving window
        cur_idx = 0
        s_idx_map = {}
        res = []
        for s_char in s:
            if s_char in p_map:
                # If s_char in p and we haven't started a moving window, start one
                if window_start == -1:
                    window_start = cur_idx

                if s_char not in s_idx_map:
                    # s_char not yet tracked -> add to map
                    s_idx_map[s_char] = [cur_idx]
                else:
                    # s_char tracked
                    s_char_indices = s_idx_map[s_char]
                    # Remove any tracked indices that have fallen behind window_start
                    clean_idx = 0
                    for s_char_index in s_char_indices:
                        if s_char_index < window_start:
                            clean_idx += 1
                        else:
                            break
                    if clean_idx == len(s_char_indices):
                        s_char_indices = []
                    else:
                        s_char_indices = s_char_indices[clean_idx:]

                    # Append current index to list
                    s_char_indices.append(cur_idx)

                    # If the number of indices surpasses the amount the char appears in p
                    if len(s_char_indices) > p_map[s_char]:
                        # Update moving window index after earliest occurrence
                        window_start = s_char_indices[0] + 1
                        # Dequeue the earliest occurrence
                        s_char_indices = s_char_indices[1:]  # Dequeue

                    # Update s_idx_map
                    s_idx_map[s_char] = s_char_indices

                # If the length of our moving window equals the length of p, we have an Anagram!
                if cur_idx - window_start == p_len - 1:
                    res.append(window_start)
                    window_start += 1
            else:
                # If s_char is not in p, then we start over!
                s_idx_map.clear()
                window_start = -1

            cur_idx += 1

        return res

    def characterReplacement(self, s: str, k: int) -> int:
        # 424
        # Example:
        #   Input: s = "AABABBA", k = 1
        #   Output: 4 (replace 'A' at idx 3 with 'B')
        # Naive implementation
        # Also misguided -> Only looks forward in s, not back. Needs to be revised.
        res = 0
        prev_char = ''
        s_len = len(s)
        for i in range(s_len):
            s_char = s[i]
            if s_char != prev_char:
                prev_char = s_char
                running_count = 1
                k_counter = 0
                while k_counter <= k and (i + running_count) < s_len:
                    next_char = s[i + running_count]
                    if next_char != s_char:
                        k_counter += 1
                        if k_counter > k:
                            break
                    running_count += 1
                if running_count > res:
                    res = running_count
        return res

    def mergeAlternately(self, word1: str, word2: str) -> str:
        # 424
        # Speed : 60%
        # Memory: 44%
        res = ''
        len1 = len(word1)
        len2 = len(word2)
        for i in range(min(len1, len2)):
            res += word1[i]
            res += word2[i]
        res += word1[i+1:]
        res += word2[i+1:]
        return res

    countBitsAns = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3,
                    2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3, 3, 4,
                    2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5,
                    4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
                    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3]

    def countBits(self, n: int) -> List[int]:
        # 338
        # Speed : 65%
        # Memory: 9%
        # Uses built-in functions, but still not great on memory
        cur_max = len(self.countBitsAns) - 1
        if n > cur_max:
            # Need to calculate up to n
            while cur_max < n:
                cur_max += 1
                bn = bin(cur_max)
                self.countBitsAns.append(bn.count('1'))
        return self.countBitsAns[:n+1]

    def countBits_old(self, n: int) -> List[int]:
        # 338
        # Speed : 5%
        # Memory: 8%
        # Doesn't use several, useful, fast, built-in functions
        cur_max = len(self.countBitsAns) - 1
        if n > cur_max:
            # Need to calculate up to n
            while cur_max < n:
                cur_max += 1
                self.countBitsAns.append(self._num_binary_ones(cur_max))
        return self.countBitsAns[:n+1]

    def _num_binary_ones(self, n: int) -> int:
        res = 0
        while n > 0:
            if n % 2 == 1:
                res += 1
                n -= 1
            n /= 2
        return res

    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # 1071
        # Speed : 78%
        # Memory: 20%

        res = ''
        cur_divisor = ''

        for i, c in enumerate(str1):
            cur_divisor += c
            if self._isDivisorOf(cur_divisor, str1) and self._isDivisorOf(cur_divisor, str2):
                res = cur_divisor
        return res

    def _isDivisorOf(self, divisor: str, quotient: str):
        len_d = len(divisor)
        len_q = len(quotient)
        if len_d > len_q or len_q % len_d != 0:
            return False
        return quotient == (divisor * int(len_q / len_d))

    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        # 1431
        # Speed : 57%
        # Memory: 11%
        max_c = max(candies)
        return [(c + extraCandies) >= max_c for c in candies]

    def maxArea_naive(self, height: List[int]) -> int:
        # 11
        # Naive way is O(n^2)
        res = 0
        for i, a in enumerate(height):
            for j, b in enumerate(height):
                water = abs(j - i) * min(a, b)
                if water > res:
                    res = water
        return res

    def maxArea(self, height: List[int]) -> int:
        # 11
        # This solution is O(n)
        # Speed : 86%
        # Memory: 22%
        res = 0
        i = 0
        j = len(height) - 1
        while i < j:
            a = height[i]
            b = height[j]
            m = min(a, b)
            water = (j - i) * m
            if water > res:
                res = water

            # Should we move i or j inward?
            # Move the pointer that is on the min
            if a == m:
                i += 1
            else:
                j -= 1
        return res

    def findMaxAverage(self, nums: List[int], k: int) -> float:
        # 643
        # Speed : 6%
        # Memory: 5%
        # TODO: Improve, both super slow and space inefficient
        if len(nums) == 1:
            return nums[0] * 1.0

        avgs = []
        sums = []
        res = None
        for i, n in enumerate(nums):
            avg_ = (n * 1.0) / (k * 1.0)
            avgs.append(avg_)
            if i == 0:
                sums.append(avg_)
            elif i < (k - 1):
                sums.append(avg_ + sums[i - 1])
            elif i == (k - 1):
                rolling_sum = avg_ + sums[i - 1]
                res = rolling_sum
                sums.append(rolling_sum)
            else:
                rolling_sum = avg_ + sums[i - 1] - avgs[i - k]
                if res is None or res < rolling_sum:
                    res = rolling_sum
                sums.append(rolling_sum)

        return res

    def pairSum(self, head: Optional[ListNode]) -> int:
        # 2130
        # Speed : 46%
        # Memory: 19%
        if head is None:
            return 0

        nums = []
        cur_node = head
        while cur_node is not None:
            nums.append(cur_node.val)
            cur_node = cur_node.next

        res = None
        nums_size = len(nums)
        for i in range(int(nums_size / 2)):
            sum_ = nums[i] + nums[nums_size - 1 - i]
            if res is None or sum_ > res:
                res = sum_
        return res

    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        # 605
        # Speed : 79%
        # Memory: 9%
        bed_len = len(flowerbed)
        if n == 0:
            return True
        elif bed_len == 0:
            return False
        elif bed_len == 1 and flowerbed[0] == 0 and n == 1:
            return True

        zero_count = 0
        only_zeros = True
        can_plant_count = 0
        for i, f in enumerate(flowerbed):
            if f == 1:
                if only_zeros:  # Special handling for bed that starts with empty slots
                    can_plant_count += int(zero_count / 2)
                else:
                    can_plant_count += int((zero_count - 1) / 2)
                only_zeros = False

                if can_plant_count >= n:
                    return True
                zero_count = 0
            else:
                zero_count += 1

        if only_zeros:
            return int((bed_len + 1) / 2) >= n

        # Empty slots at the end have more wiggle room than empty slots in the middle
        # Similar to the edge case for starting with multiple empty slots
        can_plant_count += int(zero_count / 2)
        if can_plant_count >= n:
            return True

        return False

    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        # 2215
        # Speed : 60%
        # Memory: 68%
        set1 = set(nums1)
        set2 = set(nums2)
        res1 = list(set1 - set2)
        res2 = list(set2 - set1)
        return [res1, res2]

    def maxProfit(self, prices: List[int], fee: int) -> int:
        if len(prices) <= 1:
            return 0

        sum = 0
        for p in prices[1:]:
            pass
        return 0

    tribonacci_ans = [0, 1, 1, 2, 4, 7, 13, 24]

    def tribonacci(self, n: int) -> int:
        # 1137
        # Speed : 70%
        # Memory: 15%
        i = len(self.tribonacci_ans)
        while i <= n:
            self.tribonacci_ans.append(
                self.tribonacci_ans[i - 3] +
                self.tribonacci_ans[i - 2] +
                self.tribonacci_ans[i - 1]
            )
            i += 1
        return self.tribonacci_ans[n]

    def minFlips(self, a: int, b: int, c: int) -> int:
        # 1318
        # Speed : 19%
        # Memory: 55%
        bin_a = str(bin(a))[2:]
        bin_b = str(bin(b))[2:]
        bin_c = str(bin(c))[2:]
        max_len = max(len(bin_a), len(bin_b), len(bin_c))
        bin_a = bin_a.rjust(max_len, '0')
        bin_b = bin_b.rjust(max_len, '0')
        bin_c = bin_c.rjust(max_len, '0')

        res = 0
        for i, a_bit_ in enumerate(bin_a):
            a_bit_ = int(a_bit_)
            a_bit = bool(a_bit_)
            b_bit_ = int(bin_b[i])
            b_bit = bool(b_bit_)
            c_bit = bool(int(bin_c[i]))
            if c_bit and not (a_bit or b_bit):
                res += 1
            elif not c_bit:
                res += (a_bit_ + b_bit_)
        return res

if __name__ == '__main__':
    sol = Solution()
