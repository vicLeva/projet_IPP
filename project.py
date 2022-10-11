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
        filename: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        interaction_dict (dict): a dictionnary containing nodes as key and interacting nodes as values
    """
    interaction_dict = dict()
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content:
            split = re.split(SEP, line.rstrip())
            if split[0] == split[1]: continue #X X CASE

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
        filename: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

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
        filename: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

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
        filename: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

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
    """Reads a file and verify if it is an interaction network file

    Args:
        filename: a file

    Raises:
        OSError: raises error if the path to the file is wrong or the file does not exist

    Returns:
        True if the file is an interaction network file
        else False
    """
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
        filename: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        the number of vertices (nodes) described in the input file
    """
    return len(read_interaction_file_dict(filename))

#2.1.2
def count_edges(filename):
    """Reads a file of interaction network
    Return the number of edges in the interaction network

    Args:
        filename: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

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
        fileout: an output file

    Returns:
        fileout: an interaction network file
    """
    with open(fileout, "w") as handle:
        handle.write(str(len(interactions_list)) + "\n")
        for inter in interactions_list:
            handle.write(inter[0] + "\t" + inter[1] + "\n")

def clean_interactome(filein, fileout):
    """Reads a file of interaction network
    Return a cleaned interaction network file without redundant interactions and homodimers

    Args:
        filein: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line
        fileout: an output file

    Returns:
        fileout: a cleaned interaction network file without redundant interactions and homodimers
    """
    with open(filein) as content:
        interaction_list = list()
        content.readline() #skip 1st line
        for line in content.readlines():
            split = re.split(SEP, line.rstrip())
            if (split[1], split[0]) not in interaction_list and split[1] != split[0]:
                interaction_list.append(tuple(split))
    
    write_interaction_file_from_list(interaction_list, fileout)

#2.2.1
def get_degree(file, prot):
    """Reads a file of interaction network and return the degree of a protein

    Args:
        file: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line
        prot (str): the protein for which we are looking for the degree

    Returns:
        the degree of the protein
    """
    return len(read_interaction_file_dict(file)[prot])

#2.2.2
def get_max_degree(file):
    """Reads a file of interaction network and return the protein(s) with the maximum degree

    Args:
        file: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        the protein(s) with the highest degree in the file
    """
    interaction_dict = read_interaction_file_dict(file)
    max_degree = max(len(int_list) for int_list in interaction_dict.values())
    return [prot for prot, int_list in interaction_dict.items() if len(int_list)==max_degree], \
           max_degree

#2.2.3
def get_ave_degree(file):
    """Reads a file of interaction network and return the average degree of the proteins

    Args:
        file: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line

    Returns:
        the average degree of the proteins in the file
    """
    ints_dict = read_interaction_file_dict(file)
    return sum(len(int_list) for int_list in ints_dict.values()) / len(ints_dict)

#2.2.4
def count_degree(file, deg):
    """Reads a file of interaction network and return the number of proteins with a degree equals to deg

    Args:
        file: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line
        deg (int): the degree we are looking for in the file

    Returns:
        the number of protein(s) in the file which have a degree equals to deg
    """
    ints_dict = read_interaction_file_dict(file)
    return sum(1 for prot in ints_dict if len(ints_dict[prot]) == deg)

#2.2.5
def histogram_degree(file, dmin, dmax):
    """Reads a file of interaction network and print for each value i between the interval (dmin, dmax) the number of protein in the file with a degree equals to i

    Args:
        file: an interaction network file with the number of interaction on the first line and two interacting nodes on each next line
        dmin (int): the lower bound of the interval
        dmax (int): the upper bound of the interval

    Prints:
        the number of protein with a degree equals to i for each value i between the interval (dmin, dmax)
    """
    for i in range(dmin, dmax+1):
        print(i, "*"*count_degree(file, i))


#3.1.1
#In the histogram_degree function, the file is read dmax - dmin times (one time in each loop iteration)


if __name__ == "__main__":
    print(histogram_degree("resources/toy_example.txt", 1, 3))
    #start_time = time.time()
    #clean_interactome("bs2/projet_IPP/Human_HighQuality.txt", "bs2/projet_IPP/Human_HighQualityOut.txt")
    #print("--- %s seconds ---" % (time.time() - start_time))
