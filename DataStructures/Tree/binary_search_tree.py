import bst_node as bs

def new_map():
    """Crea una tabla de símbolos ordenada vacía basada en un BST."""
    my_bst = {"root": None}
    return my_bst
 
 
def default_compare(key, element):
    """
    Compara una llave con la llave de un nodo.
    Retorna 0 si son iguales, 1 si key es mayor, -1 si key es menor.
    """
    node_key = bst.get_key(element)
    if key == node_key:
        return 0
    elif key > node_key:
        return 1
    return -1


def size_tree(root):
    if root is None:
        return 0
    return  1+size_tree(root.left)+size_tree(root.right)





