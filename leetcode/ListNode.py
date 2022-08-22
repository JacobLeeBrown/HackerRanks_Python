from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def from_list(nums: List[int]) -> Optional[ListNode]:
    if len(nums) == 0:
        return None
    else:
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


def to_list(head: Optional[ListNode]) -> List[int]:
    res = []
    while head is not None:
        res.append(head.val)
        head = head.next
    return res
