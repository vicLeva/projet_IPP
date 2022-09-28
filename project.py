import re
import numpy as np
import time

def read_interaction_file_dict(filename):
    interaction_dict = dict()
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())
            if split[0] in interaction_dict:
                interaction_dict[split[0]].append(split[1])
            else:
                interaction_dict[split[0]] = [split[1]]
    return interaction_dict

def read_interaction_file_list(filename):
    with open(filename) as content:
        interaction_list = [0] * int(content.readline())
        index = 0
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())
            interaction_list[index] = tuple(split)
            index += 1
       
    return interaction_list

#print(read_interaction_file_dict("bs2/projet_IPP/toy_example.txt"))
#print(read_interaction_file_dict("Human_HighQuality.txt"))

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


start_time = time.time()
print(read_interaction_file_mat("Human_HighQuality.txt"))
print("--- %s seconds ---" % (time.time() - start_time))