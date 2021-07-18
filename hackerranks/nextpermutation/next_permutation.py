
def next_permutation(nums):
    """ Rearrange list into lexicographically next greater permutation. If such
    an arrangement is not possible (list is already in greatest permutation),
    then return the least permutation (numbers sorted in ascending order).
    Operation is in-place and uses constant extra memory. Assumes `nums`
    contains only non-negative elements.

    Parameters
    ----------
    nums : list of int
        Target list to rearrange in-place to next greater permutation
    """

    nums_len = len(nums)

    # If the list is empty or singleton, no work to be done
    if nums_len <= 1:
        return

    # Check if list is already in greatest permutation (elements in descending
    # order). Simultaneously search for least-significant (right most) index to
    # begin permutation operation.
    start = -1
    for i in range(nums_len-2, -1, -1):
        if nums[i] < nums[i+1]:
            start = i
            break

    # If we did not update start, list is already at greatest permutation
    # To get least permutation, simply reverse the list
    if start == -1:
        nums.reverse()
        return

    # If we've made it here, perform permute operation
    _permute(nums, start)


def _permute(nums, start):
    """Permute nums[start:]. This only considers the 'least significant`
    elements (from `start` to end) since permuting them will result in the next
    permutation for the whole list thanks to the pre-processing of determining
    the correct `start` index.
    """
    swap_idx = _find_permute_min_idx(nums, start)
    # Perform initial permute swap
    nums[start], nums[swap_idx] = nums[swap_idx], nums[start]
    # Reverse the rest of the list, which is guaranteed to be in descending
    # order at this point, and we want it in ascending order
    _partial_reverse(nums, start+1)


def _find_permute_min_idx(nums, start):
    """Find index of minimum element in nums[start+1:] that is greater than
    nums[start]. In other words, find the index to swap nums[start] with, so it
    must be strictly greater so we don't swap duplicates.
    """
    low_bound = nums[start]
    cur_min = -1
    min_idx = -1
    for i in range(start+1, len(nums)):
        cur = nums[i]
        # Only consider elements greater than nums[start]
        if cur > low_bound:
            if (cur_min == -1) or (cur_min >= cur):
                cur_min = cur
                min_idx = i
    return min_idx


def _partial_reverse(a, start):
    """Reverse array `a` from `start` to end (a[start:]) in-place and with
    constant extra memory.
    """
    rev_len = int((len(a) - start)/2)
    for i in range(rev_len):
        idx_1 = start + i
        idx_2 = -(i + 1)
        a[idx_1], a[idx_2] = a[idx_2], a[idx_1]
