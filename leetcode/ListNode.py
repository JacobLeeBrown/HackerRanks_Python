from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def from_list(nums: List[int]) -> Optional[ListNode]:
    if len(nums) == 0:
        return None
    prev_node = None
    head = None
    for i in nums:
        node = ListNode(i, None)
        if head is None:
            head = node
        if prev_node is not None:
            prev_node.next = node
        prev_node = node
    return head


def to_list(head: Optional[ListNode], limit=-1) -> List[int]:
    res = []
    i = 0
    while head is not None and (limit == -1 or i < limit):
        res.append(head.val)
        head = head.next
        i += 1
    return res


def from_list_and_tail_pointer(nums: List[int], tail_next_idx: int) -> Optional[ListNode]:
    if len(nums) == 0:
        return None
    head = None
    node = None
    prev_node = None
    j = 0
    cycle_node = None
    for i in nums:
        node = ListNode(i, None)
        if head is None:
            head = node
        if prev_node is not None:
            prev_node.next = node
        prev_node = node
        if j == tail_next_idx:
            cycle_node = node
        j += 1

    if tail_next_idx >= 0:
        node.next = cycle_node
    return head
