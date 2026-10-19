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
    node_key = bs.get_key(element)
    if key == node_key:
        return 0
    elif key > node_key:
        return 1
    return -1

def insert_node(root, key, value):
    """Inserta (o actualiza) recursivamente la pareja llave-valor y retorna la raíz del subárbol."""
    if root is None:
        return bs.new_node(key, value)
 
    cmp = default_compare(key, root)
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value
 
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
 
def put(my_bst, key, value):
    """Agrega una pareja llave-valor al árbol. Si la llave existe, actualiza el valor."""
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def size_tree(root):
    if root is None:
        return 0
    return  1+size_tree(root.left)+size_tree(root.right)

def size(my_bst):
    return size_tree(my_bst['root'])

def get_node(root, key):
    """Busca recursivamente la llave y retorna el nodo encontrado, o None si no existe."""
    if root is None:
        return None
 
    cmp = default_compare(key, root)
    if cmp < 0:
        return get_node(root["left"], key)
    elif cmp > 0:
        return get_node(root["right"], key)
    return root

def get(my_bst, key):
    """Retorna el valor asociado a la llave, o None si no existe."""
    node = get_node(my_bst["root"], key)
    return bs.get_value(node)


def contains(my_bst, key):
    if get(my_bst,key)==None:
        return False
    else:
        return True

def is_empty(my_bst):
    if my_bst('root')==None:
        return False
    else:
        return True

def key_set(my_bst):
    llaves=sll.new_list()
    if my_bst is not None and my_bst['root'] is not None:
            key_set_tree(my_bst['root'],llaves)
    return llaves

def key_set_tree(node, my_list):
    if node is None:
        return my_list
    key_set_tree(node['left'], my_list)

    llave=bs.get_key(node)
    sll.add_last(my_list,llave)

    key_set_tree(node['right'], my_list)
    return my_list

def value_set(my_bst):
    llaves=sll.new_list()
    if my_bst is not None and my_bst['root'] is not None:
            value_set_tree(my_bst['root'],llaves)
    return llaves

def value_set_tree(node, my_list):
    if node is None:
        return my_list
    value_set_tree(node['left'], my_list)

    llave=bs.get_value(node)
    sll.add_last(my_list,llave)

    value_set_tree(node['right'], my_list)
    return my_list






