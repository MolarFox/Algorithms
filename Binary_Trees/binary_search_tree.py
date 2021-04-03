# MolarFox 2018
# Binary Search Tree Class


class TreeNode:
    def __init__(self, new_item=None, left=None, right=None):
        self.item = new_item
        self.left = left
        self.right = right


class BinarySearchTree:

    def __init__(self):
        self.root = None

    # -----------------------------------------------------------------------

    def find_min_aux_1(self, current):
        if current is not None:
            return self.find_min_aux_1(current.left)
        else:
            return current

    # -----------------------------------------------------------------------

    def find_min_2(self):
        if self.root is None:
            return self.root
        else:
            return self.find_min_aux_2(self.root)

    # -----------------------------------------------------------------------

    # Oman, this version works correctly :D
    def find_min_aux_2(self, current):
        if current.left is None:
            return current.item
        else:
            return self.find_min_aux_2(current.left)

