import bst_node as bs



def size_tree(root):
    if root is None:
        return 0
    return  1+size_tree(root.left)+size_tree(root.right)





