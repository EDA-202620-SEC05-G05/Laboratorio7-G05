"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """
 
import os
import csv
import datetime
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
 
 
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
 
 
def new_logic():
    analyzer = {
        'crimes': None,
        'dateIndex': None
    }
    analyzer['crimes'] = al.new_list()
    analyzer['dateIndex'] = bst.new_map()
    return analyzer
 
 
# Funciones para realizar la carga
 
def load_data(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        add_crime(analyzer, crime)
    return analyzer
 
 
# Funciones para agregar informacion al analizador
 
 
def add_crime(analyzer, crime):
    """
    funcion que agrega un crimen al catalogo
    """
    al.add_last(analyzer['crimes'], crime)
    update_date_index(analyzer['dateIndex'], crime)
    return analyzer
 
 
def update_date_index(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.
 
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    cdate = crimedate.date()
    entry = bst.get(map, cdate)
    if entry is None:
        datentry = new_data_entry(crime)
        bst.put(map, cdate, datentry)
    else:
        datentry = entry
    add_date_index(datentry, crime)
    return map
 
 
def add_date_index(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstcrimes']
    al.add_last(lst, crime)
    offenseIndex = datentry['offenseIndex']
    offensegrp = crime['OFFENSE_CODE_GROUP']
    offentry = lp.get(offenseIndex, offensegrp)
    if offentry is None:
        offentry = new_offense_entry(offensegrp, crime)
        al.add_last(offentry['lstoffenses'], crime)
        lp.put(offenseIndex, offensegrp, offentry)
    else:
        al.add_last(offentry['lstoffenses'], crime)
    return datentry
 
 
def new_data_entry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = lp.new_map(num_elements=30,
                                       load_factor=0.5)
    entry['lstcrimes'] = al.new_list()
    return entry
 
 
def new_offense_entry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = al.new_list()
    return ofentry
 
 
# ==============================
# Funciones de consulta
# ==============================
 
 
def crimes_size(analyzer):
    """
    Número de crimenes
    """
    return al.size(analyzer['crimes'])
 
 
def index_height(analyzer):
    """
    Altura del arbol
    """
    return bst.height(analyzer['dateIndex'])
 
 
def index_size(analyzer):
    """
    Numero de elementos en el indice
    """
    return bst.size(analyzer['dateIndex'])
 
 
def min_key(analyzer):
    """
    Llave mas pequena
    """
    return bst.get_min(analyzer['dateIndex'])
 
 
def max_key(analyzer):
    """
    Llave mas grande
    """
    return bst.get_max(analyzer['dateIndex'])
 
 
def get_crimes_by_range(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rango de fechas
    """
    d1 = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
    d2 = datetime.datetime.strptime(finalDate, '%Y-%m-%d').date()
    entries = bst.values(analyzer['dateIndex'], d1, d2)
    total = 0
    node = entries['first']
    while node is not None:
        total += al.size(node['info']['lstcrimes'])
        node = node['next']
    return total
 
 
def get_crimes_by_range_code(analyzer, initialDate, offensecode):
    """
    Retorna el numero de crimenes de un tipo en una fecha
    """
    d1 = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
    entry = bst.get(analyzer['dateIndex'], d1)
    if entry is None:
        return 0
    offentry = lp.get(entry['offenseIndex'], offensecode)
    if offentry is None:
        return 0
    return al.size(offentry['lstoffenses'])