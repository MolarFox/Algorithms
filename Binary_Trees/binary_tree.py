# MolarFox 2018
# Binary Tree Class


class TreeNode:
    def __init__(self, new_item=None, left=None, right=None):
        self.item = new_item
        self.left = left
        self.right = right


class BinaryTree:

    def __init__(self):
        self.root = None

    # -----------------------------------------------------------------------

    def get_height(self, node=0):
        if node is None:
            return 0

        if type(node) is int:   # Doesn't seem to like self in arg declarations
            node = self.root

        if node.left is None or node.right is None:
            if node.left is not None:
                return self.get_height(node.left) + 1
            if node.right is not None:
                return self.get_height(node.right) + 1
            return 1

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    # -----------------------------------------------------------------------

    def sum_all(self, node=0):
        if node is None:
            return 0

        if type(node) is int:   # Doesn't seem to like self in arg declarations
            node = self.root

        if node.left is None or node.right is None:
            if node.left is not None:
                return self.sum_leaves(node.left) + node.item
            if node.right is not None:
                return self.sum_leaves(node.right) + node.item
            return node.item

        return self.sum_all(node.left) + self.sum_all(node.right) + node.item

        # -----------------------------------------------------------------------

    def sum_leaves(self, node=0):
        if node is None:
            return 0

        if type(node) is int:  # Doesn't seem to like self in arg declarations
            node = self.root

        if node.left is None and node.right is None:
            return node.item

        return self.get_height(node.left) + self.get_height(node.right)


