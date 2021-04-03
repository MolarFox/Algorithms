# MolarFox 2018
# Find k-largest item in a BST


def find_largest(current, k):
    out = []

    if current.left is not None:
        out = out + find_largest(current.left)

    out = out + current.item

    if current.right is not None:
        out = out + find_largest(current.right)

    if current == self.root:
        return out[-k]
    return out
