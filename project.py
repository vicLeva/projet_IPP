import re
import numpy as np
import time
import os.path


SEP = ' |\t' #Separator = space or tab.

#1.2.1
def read_interaction_file_dict(filename):
    """Reads a file of interaction network
    Return a dictionnary containing with nodes as keys and interacting nodes as values

    Args:
        filename (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        interaction_dict (dict): a dictionnary containing nodes as key and interacting nodes as values
    """
    interaction_dict = dict()
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content:
            split = re.split(SEP, line.rstrip())

            if split[0] in interaction_dict: #X Y CASE
                interaction_dict[split[0]].add(split[1])
            else:
                interaction_dict[split[0]] = {split[1]}

            if split[1] in interaction_dict: #Y X CASE
                interaction_dict[split[1]].add(split[0])
            else:
                interaction_dict[split[1]] = {split[0]}
    return interaction_dict


#1.2.2
def read_interaction_file_list(filename):
    """Reads a file of interaction network
    Return a list containing couple of interacting nodes in tuples

    Args:
        filename (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        interaction_list (list): a list containing couples of interacting nodes in tuples
    """
    with open(filename) as content:
        try: #empty file case
            interaction_list = [0] * int(content.readline().rstrip())
        except ValueError:
            return list()
            
        index = 0
        for line in content:
            split = re.split(SEP, line.rstrip())
            interaction_list[index] = tuple(split)
            index += 1
       
    return interaction_list

#1.2.3
def read_interaction_file_mat(filename):
    """Reads a file of interaction network
    Return an adjacency matrix of interactions and the ordonnate list of nodes to read it

    Args:
        filename (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        matrix (numpy array): a adjacency matrix : 0 for non-interacting nodes, 1 for interacting nodes
        nodes_list (list): a list containing the nodes in order of the adjacency matrix
    """
    nodes_list = set() #to avoid duplicates
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content: 
            nodes_list.update(re.split(SEP, line.rstrip()))
    
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
    """Reads a file of interaction network
    Return the dictionnary, the list, the matrix and the ordonnate list to read it

    Args:
        filename (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        interaction_dict (dict): a dictionnary containing nodes as key and interacting nodes as values
        interaction_list (list): a list containing couples of interacting nodes in tuples
        mat_and_list[0] (numpy array): a adjacency matrix : 0 for non-interacting nodes, 1 for interacting nodes
        mat_and_list[1] (list): a list containing the nodes in order of the adjacency matrix

    """
    mat_and_list = read_interaction_file_mat(filename)
    return (read_interaction_file_dict(filename), 
            read_interaction_file_list(filename), 
            mat_and_list[0], 
            mat_and_list[1])

#1.2.5
#Pour un plus gros graphe d'interactions, il faudrait lire le fichier qu'une
#seule fois en créant le dict, la list et la matrice au fur et à mesure de cette
#seule lecture.

#1.2.7
def is_interaction_file(filename):
    if not os.path.isfile(filename):
        raise OSError("Wrong path or file missing.")
    else:
        if os.stat(filename).st_size == 0: return False #empty file

        count = 0
        with open(filename) as content:
            first_line = content.readline().rstrip()
            try: 
                nb_interactions = int(first_line)
            except ValueError: #first line missing or wrong format
                return False
            
            for line in content:
                split = re.split(SEP, line.rstrip())
                if len(split) != 2:
                    return False #wrong number of columns
                count += 1
            
            if count != nb_interactions: return False #wrong number in first line

        return True


#2.1.1
def count_vertices(filename):
    """Reads a file of interaction network
    Return the number of vertices in the interaction network

    Args:
        filename (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        the number of vertices (nodes) described in the input file
    """
    return len(read_interaction_file_dict(filename))

#2.1.2
def count_edges(filename):
    """Reads a file of interaction network
    Return the number of edges in the interaction network

    Args:
        filename (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        the number of edges (interactions) described in the input file
    """
    return len(read_interaction_file_list(filename))

#2.1.3
def write_interaction_file_from_list(interactions_list, fileout):
    """Reads a list of interactions
    Return an interaction network file

    Args:
        interaction_list (list): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line
        fileout (.txt) : an output file

    Returns:
        fileout (.txt) : an interaction network file
    """
    with open(fileout, "w") as handle:
        handle.write(str(len(interactions_list)) + "\n")
        for inter in interactions_list:
            handle.write(inter[0] + "\t" + inter[1] + "\n")

def clean_interactome(filein, fileout):
    """Reads a file of interaction network
    Return a cleaned interaction network file without redundant interactions and homodimers

    Args:
        filein (.txt): an interaction network file with the number of interaction on the first line and two interacting nodes on each next line
        fileout (.txt) : an output file

    Returns:
        fileout (.txt) : a cleaned interaction network file without redundant interactions and homodimers
    """
    with open(filein) as content:
        interaction_list = list()
        content.readline() #skip 1st line
        for line in content.readlines():
            split = re.split(SEP, line.rstrip())
            if (split[1], split[0]) not in interaction_list and split[1] != split[0]:
                interaction_list.append(tuple(split))
    
    write_interaction_file_from_list(interaction_list, fileout)


if __name__ == "__main__":
    pass
    #start_time = time.time()
    #clean_interactome("bs2/projet_IPP/Human_HighQuality.txt", "bs2/projet_IPP/Human_HighQualityOut.txt")
    #print("--- %s seconds ---" % (time.time() - start_time))
