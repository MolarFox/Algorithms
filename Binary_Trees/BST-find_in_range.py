# MolarFox 2018
# Returns all elements between two vals in a BST


def between_vals(current, a, b):
    out = []
    if current is None:
        return out

    if not (a < current.item < b):
        return out

    if current.left is not None:
        out = out + between_vals(current.left, a, b)

    if current.right is not None:
        out = out + between_vals(current.right.item, a, b)

    return out
