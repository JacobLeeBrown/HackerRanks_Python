# Given a list of numbers,
# Return the same list rearranged into the lexicographically next greater permutation. Ex: [1, 3, 2] -> [2, 1, 3]
#   If such an arrangement is not possible (list already lexicographically greatest order), then return lowest order
#       Ex: [3, 2, 1] -> [1, 2, 3]
# The replacement must be in place and use only constant extra memory.


def next_permutation(nums):
    """ Rearrange list into lexicographically next greater permutation. If such
    an arrangement is not possible (list is already in greatest permutation),
    then return the least permutation (numbers sorted in ascending order).
    Operation is in-place and uses constant extra memory.

    Parameters
    ----------
    nums : list of int
        Target list to rearrange in-place to next greater permutation
    """

    nums_len = len(nums)

    # If the list is empty or singleton, no work to be done
    if nums_len <= 1:
        return

    # To get next greater permutation, take last number (swap) and, scanning
    # from right to left through the list, insert before first number that is
    # less than swap
    swap = nums[nums_len-1]
    for i in range(nums_len-2, -1, -1):
        if swap > nums[i]:
            nums.insert(i, swap)
            nums.pop()  # Remove swap from end of list
            return

    # If we make it here, list is already at greatest permutation
    # To get least permutation, simply reverse the list
    nums.reverse()
    return
