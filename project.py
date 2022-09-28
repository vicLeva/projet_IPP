import re
import numpy as np
import time

#1.2.1
def read_interaction_file_dict(filename):
    interaction_dict = dict()
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())

            if split[0] in interaction_dict: #X Y CASE
                interaction_dict[split[0]].append(split[1])
            else:
                interaction_dict[split[0]] = [split[1]]

            if split[1] in interaction_dict: #Y X CASE
                interaction_dict[split[1]].append(split[0])
            else:
                interaction_dict[split[1]] = [split[0]]

    return interaction_dict

#1.2.2
def read_interaction_file_list(filename):
    with open(filename) as content:
        interaction_list = [0] * int(content.readline())
        index = 0
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())
            interaction_list[index] = tuple(split)
            index += 1
       
    return interaction_list

#1.2.3
def read_interaction_file_mat(filename):
    nodes_list = set() #to avoid duplicates
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content.readlines(): 
            nodes_list.update(re.split(' |\t', line.rstrip()))
    
    nodes_list = list(nodes_list)
    inters_list = read_interaction_file_list(filename)

    size = len(nodes_list)
    matrix = np.zeros((size, size),dtype=int)

    for i, j in inters_list:
        idx1 = nodes_list.index(i)
        idx2 = nodes_list.index(j)
        matrix[idx1, idx2] = 1
        matrix[idx2, idx1] = 1

    return (matrix, nodes_list)

#1.2.4
def read_interaction_file(filename):
    mat_and_list = read_interaction_file_mat(filename)
    return (read_interaction_file_dict(filename), 
            read_interaction_file_list(filename), 
            mat_and_list[0], 
            mat_and_list[1])

#1.2.5
#Pour un plus gros graphe d'interactions, il faudrait lire le fichier qu'une
#seule fois en créant le dict, la list et la matrice au fur et à mesure de cette
#seule lecture.

#2.1.1
def count_vertices(filename):
    return len(read_interaction_file_dict(filename))

#2.1.2
def count_edges(filename):
    return len(read_interaction_file_list(filename))

#2.1.3
def write_interaction_file_list(interactions_list, fileout):
    with open(fileout, "w") as handle:
        handle.write(str(len(interactions_list)) + "\n")
        for inter in interactions_list:
            handle.write(inter[0] + " " + inter[1] + "\n")

def clean_interactome(filein, fileout):
    with open(filein) as content:
        interaction_list = list()
        content.readline() #skip 1st line
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())
            if (split[1], split[0]) not in interaction_list or split[1] != split[0]:
                interaction_list.append(tuple(split))
    
    write_interaction_file_list(interaction_list, fileout)


#start_time = time.time()
#clean_interactome("bs2/projet_IPP/Human_HighQuality.txt", "bs2/projet_IPP/Human_HighQualityOut.txt")
#print("--- %s seconds ---" % (time.time() - start_time))