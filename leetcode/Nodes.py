from typing import List, Optional


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tnodes_from_array(vals: List[List[int]]) -> Optional[TreeNode]:
    if len(vals) == 0:
        return None
    root = TreeNode(vals[0][0])
    nodes = [root]
    for i, node_vals in enumerate(vals[1:]):
        parent_node = nodes[i]

        if node_vals[0] is None:
            nodes.append(None)
        else:
            left_node = TreeNode(node_vals[0])
            parent_node.left = left_node
            nodes.append(left_node)

        if node_vals[1] is None:
            nodes.append(None)
        else:
            right_node = TreeNode(node_vals[1])
            parent_node.right = right_node
            nodes.append(right_node)

    return root
