import csv
import numpy as np
import time

#1.2.1
def read_interaction_file_dict(filename):
    """_summary_

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    #creating empty dictionnary
    interactions = {}
    
    #opening file
    csvfile = open(filename, 'r')
    #finding the delimiter (from line 2)
    next(csvfile)
    dialect = csv.Sniffer().sniff(csvfile.readline())
    #return at the top of the file
    csvfile.seek(0)

    #reading the file as a csv and skip the first line
    graph = csv.reader(csvfile, delimiter=dialect.delimiter)
    next(graph)

    for line in graph:
        if line[0] or line[1] not in interactions.keys():
            interactions[line[0]] = []
            interactions[line[1]] = []

    
    #return at the top of the csv file and skip first line again
    csvfile.seek(0)
    next(graph)

    #fill the lists
    for line in graph:
        if line[1] not in interactions[line[0]]:
            interactions[line[0]].append(line[1])
        if line[0] not in interactions[line[1]]:
            interactions[line[1]].append(line[0])

    return interactions

    
#read_interaction_file_dict("Human_HighQuality.txt")


#1.2.2
def read_interaction_file_list(filename):
    #creating empty list
    interactions = []

    #opening file
    csvfile = open(filename, 'r')
    next(csvfile)
    dialect = csv.Sniffer().sniff(csvfile.readline())
    csvfile.seek(0)

    #reading the file as a csv
    graph = csv.reader(csvfile, delimiter=dialect.delimiter)
    next(graph)

    #make tuples and putting them into a list
    for line in graph:
        couple = (line[0], line[1])
        interactions.append(couple)
    
    return interactions

#read_interaction_file_list("toy_example.txt")


#1.2.3
def read_interaction_file_mat(filename):
    #create the dictionnary of interactions
    interactions = read_interaction_file_dict(filename)
    
    #make the ordonnate list of the interactions from the dictionnary
    ordonnate_list = []
    for key in interactions.keys():
        ordonnate_list.append(key)

    #initiate the matrix with the right size and all value == 0
    nb_of_interactions = len(interactions)
    mat = np.zeros((nb_of_interactions,nb_of_interactions), dtype=int)

    #for every interaction describe in the dictionnary, replace 0 by 1 in the matrix. indexes of the ordonnate list are used
    for inter in interactions.items():
        for i in inter[1]:
            mat[ordonnate_list.index(inter[0])][ordonnate_list.index(i)] = 1
    #print(mat)
    
    return [mat, ordonnate_list]


""" t0=time.time()
read_interaction_file_mat("Human_HighQuality.txt")
t1=time.time()
print(str(t1-t0) + "secondes")


t0=time.time()
print(read_interaction_file_mat("toy_example.txt"))
t1=time.time()
print(str(t1-t0) + "secondes") """

#1.2.3
def read_interaction_file(filename):
    res = [read_interaction_file_dict(filename), read_interaction_file_list(filename), read_interaction_file_mat(filename)]
    return res

#read_interaction_file("Human_HighQuality.txt")




#2.1.1
def count_vertices(filename):
    graph = read_interaction_file_dict(filename)
    nb_of_vertices = len(graph)
    return nb_of_vertices 

#print(count_vertices("Human_HighQuality.txt"))


#2.1.2
def count_edges(filename):
    graph = read_interaction_file_list(filename)
    nb_of_edges = len(graph)
    return nb_of_edges

#print(count_edges("Human_HighQuality.txt"))


#2.1.3
def clean_interactome(filein, fileout):œ
    graph = read_interaction_file_list(filein)
    with open ()
