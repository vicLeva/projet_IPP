import re
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

SEP = ' |\t' #Separator = space or tab.

def vertices_generator(n):
    return [str(i) for i in range(n)]


class Interactome:
    """
    Models an interactome, builds it from a file, then computes global or local metrics (density, degree, clustering coef, ...)
    
    Attributes:
        int_list (list): the list of all proteins interactions of the interactome
        int_dict (dict): keys -> proteins, values -> set of proteins that interact with the key
        int_matrix (numpy array): 2D adjacency matrix of the interactome, needs self.proteins to be used
        proteins (list): list of all the interactome proteins, in the order of the int_matrix
    """
    #3.2.3
    def __init__(self, filename=None, algo=None, proteins=None, proba=None):
        """Constructor, inits every attributes in 1 file read, in case of filename, 
        else with an algorithm to generate the graph
        
        Args:
            filename (str): The file path (must be a clean file !)
            algo (str): The generation graph algorithm {"erdos_renyi", "scale_free"}
            proteins (list): The nodes of the generated graph
            proba (float): In case of "erdos_renyi", the proba for each edge to be present
        """

        if filename != None:
            self.build_from_file(filename)
        
        else:
            self.proteins = proteins
            self.int_dict = dict([(prot, set()) for prot in proteins])
            self.int_list = list()

            if algo == "erdos_renyi":
                self.build_from_random(proba)
            elif algo == "scale_free":
                self.build_from_scalefree()

        #CONSTRUCT MAT
        size = len(self.proteins)
        self.int_matrix = np.zeros((size, size), dtype=int)

        for x, y in self.int_list:
            idx1 = self.proteins.index(x)
            idx2 = self.proteins.index(y)
            self.int_matrix[idx1, idx2] = 1
            self.int_matrix[idx2, idx1] = 1



    def build_from_file(self, filename):
        """Constructor side method, inits every attributes in 1 file read
        
        Args:
            filename (str): The file path (must be a clean file !)
        """
        with open(filename) as content:
            self.proteins = list()
            self.int_dict = dict()
            self.int_list = [0] * int(content.readline().rstrip())

            index = 0
            for line in content:
                split = re.split(SEP, line.rstrip())

                #CONSTRUCT LIST
                self.int_list[index] = tuple(split)
                index += 1

                #CONSTRUCT DICT
                if split[0] in self.proteins:
                    self.int_dict[split[0]].add(split[1])
                else:
                    self.proteins.append(split[0])
                    self.int_dict[split[0]] = {split[1]}

                if split[1] in self.proteins:
                    self.int_dict[split[1]].add(split[0])
                else:
                    self.proteins.append(split[1])
                    self.int_dict[split[1]] = {split[0]}

    
    def build_from_random(self, q):
        """Constructor side method, inits every attributes while generating a random graph with erdos_renyi algorithm
        
        Args:
            q (float): The proba for each edge to be present
        """
        for i in range(len(self.proteins)):
            for j in range(i+1, len(self.proteins)):
                if random.random() < q:
                    self.int_list.append((self.proteins[i], self.proteins[j]))
                    self.int_dict[self.proteins[i]].add(self.proteins[j])
                    self.int_dict[self.proteins[j]].add(self.proteins[i])

    def build_from_scalefree(self):
        """
        Constructor side method, inits every attributes while generating a random graph with erdos_renyi algorithm
        """
        #start with a 2 nodes clique
        total_deg = 2
        self.int_list.append((self.proteins[0], self.proteins[1]))
        self.int_dict[self.proteins[0]].add(self.proteins[1])
        self.int_dict[self.proteins[1]].add(self.proteins[0])

        for i in range(2, len(self.proteins)):
            nb_new_interaction = 0
            for j in range(i):
                # proba =  deg(proteins[j]) / sum(all degrees)
                if random.random() < len(self.int_dict[self.proteins[j]]) / total_deg:
                    self.int_list.append((self.proteins[i], self.proteins[j]))
                    self.int_dict[self.proteins[i]].add(self.proteins[j])
                    self.int_dict[self.proteins[j]].add(self.proteins[i])
                    nb_new_interaction += 1
            total_deg += nb_new_interaction * 2
            



    #SETTERS
    def set_int_list(self, new_list):
        self.int_list = new_list
    def set_int_dict(self, new_dict):
        self.int_dict = new_dict
    def set_proteins(self, new_proteins):
        self.proteins = new_proteins

    #GETTERS
    def get_int_list(self):
        return self.int_list
    def get_int_dict(self):
        return self.int_dict
    def get_proteins(self):
        return self.proteins

    def display(self):
        """
        Plots a graphic representation of the graph (graph must be ~small)
        """
        G = nx.Graph(self.int_dict)
        """ G.add_edges_from(self.int_list)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=False) """
        nx.draw(G, with_labels=True)
        plt.draw()
        plt.show()

    #3.2.4
    #MEMBER METHODS
    def count_vertices(self):
        """Counts the number of vertices of the interactome
        
        Returns:
            the number of vertices (nodes, proteins)
        """
        return len(self.proteins)

    def count_edges(self):
        """Counts the number of edges of the interactome
        
        Returns:
            the number of edges (interactions)
        """
        return len(self.int_list)

    def get_degree(self, prot):
        """Computes the degree of a protein 
        (i.e. the number of edges/interactions from this prot)

        Args:
            prot (str): the protein of which we want to find the degree
        
        Returns:
            the degree of the protein prot
        """
        return len(self.int_dict[prot])

    def get_max_degree(self):
        """Computes the max degree of an interactome
 
        Returns:
            the proteins with the highest degree AND the max degree in a tuple
        """
        max_degree = max(len(int_list) for int_list in self.int_dict.values())
        return [prot for prot, int_list in self.int_dict.items() if len(int_list)==max_degree], \
               max_degree

    def get_ave_degree(self):
        """Computes the average degree of an interactome
 
        Returns:
            the average of all protein degrees of an interactome
        """
        return sum(len(int_list) for int_list in self.int_dict.values()) / len(self.int_dict)

    def count_degree(self, deg):
        """Computes the number of proteins of particular degree

        Args:
            deg (int): the degree of which we want the number of nodes
 
        Returns:
            the number of proteins of degree deg
        """
        return sum(1 for prot in self.int_dict if len(self.int_dict[prot]) == deg)

    def histogram_degree(self, dmin, dmax):
        """Displays an ASCII histogram of the degrees of an interactome between intervals

        Args:
            dmin (int): the lower bound of the interval
            dmax (int): the upper bound of the interval
        """
        for i in range(dmin, dmax+1):
            print(i, "*"*self.count_degree(i))

    #3.3.1
    def density(self):
        """Computes the density of an interactome (i.e. the ratio: edges / max edges)
 
        Returns:
            the density of the interactome
        """
        verts = self.count_vertices()
        edges = self.count_edges()
        return 2*edges / (verts*(verts - 1))

    #3.3.2
    def clustering(self, prot):
        """Computes the clustering coefficient of a protein
        Uses the 2n(prot) / k(k-1) formula with
        n(x) = number of neighbours edges around node x
        k = number of neighbours

        Args:
            prot (str): the protein of which we want the clustering coefficient
 
        Returns:
            the local clustering coefficient of a protein
        """
        neighbours = self.int_dict[prot]
        nb_neigh = len(neighbours)

        if nb_neigh <= 1: return 0

        sum_edges = 0
        for n in neighbours: #for every neighbours n of prot
            for nn in self.int_dict[n]: #for every neighbours of n
                if nn in neighbours: #if nn (n neighbour) is a neighbour of prot
                    sum_edges += 1
        
        # sum_edges and not 2*sum_edges because we counted every edge twice
        return sum_edges / (nb_neigh * (nb_neigh-1))



    #5.1.2
    def count_CC(self):
        """Finds the number of connected component in the graph, and how many proteins are in each of them

        Returns:
            The number of connected component, and a list of their sizes
        """
        lcc = self.compute_CC()
        nb_CC = max(lcc)
        CC_sizes_list = [0] * nb_CC
        for id_CC in lcc:
            CC_sizes_list[id_CC-1] += 1
        return nb_CC, CC_sizes_list

    #5.1.3
    def write_CC(self):
        """Write a file containing a line for each connected component.
        Each line contains the size of the connected component as the first character, and then the list of their proteins
        """
        content = list(map(str, self.count_CC()[1]))
        for id_prot, id_CC in enumerate(self.compute_CC()):
            content[id_CC-1] += "\t" + str(self.proteins[id_prot])

        with open("CCs.txt", "w") as file:
            file.write('\n'.join(content))

    #5.1.4
    def extract_CC(self, prot):
        """Return all the proteins of the connected component to which prot belong

        Args:
            prot (str): the protein with which the function will start the path

        Returns:
            the list of all proteins in the connected component of prot
        """
        visited = []
        queue = [prot] #a list used as a queue

        while len(queue) != 0:
            #browse the neighbours of the first protein of the queue with the dictionnary
            for neighbour in self.int_dict[queue[0]]:
                #add the neighbours to the end of the queue if it is the first time ecountering them
                if neighbour not in queue and neighbour not in visited:
                    queue.append(neighbour)

            #removing first protein of the queue and adding it to the final list
            visited.append(queue.pop(0))
        
        return visited

    #5.1.5
    def compute_CC(self):
        """Finds to which connected component belongs each protein of the graph

        Returns:
            a list in which each element correspond to the connected component that the protein with the same id in the list of protein belong
        """
        lcc = [-1] * len(self.proteins)
        
        #for each protein (starting with the first of the list) compute their connected component if they are still in the "-1" group
        id_CC = 1
        for index, prot in enumerate(self.proteins):
            if lcc[index] == -1:
                #change the group of each protein of the connected component in the dictionnary
                for prot_connected in self.extract_CC(prot):
                    lcc[self.proteins.index(prot_connected)] = id_CC
                #go to the next connected component
                id_CC +=1
                
        return lcc


if __name__ == "__main__":
    #Constructor of Interactome how to use:
    #from file : Interactome(filename="filename")
    #from erdos-renyi gen. graph : Interactome(algo="erdos_renyi", proteins=proteins_list, proba=q)
    #from barabasi-albert gen. graph : Interactome(algo="scale_free", proteins=proteins_list)

    #example of Human_HighQuality.txt with basic functions
    """
    interactome_human = Interactome(filename="resources/Human_HighQuality.txt")
    print(interactome_human.count_vertices(), "vertices")
    print(interactome_human.count_edges(), "edges")
    print(f"max degree: {interactome_human.get_max_degree()}")
    print(f"average degree: {interactome_human.get_ave_degree()}")
    print(f"density: {interactome_human.density()}")
    print(f"clustering coef of ATX1_HUMAN: {interactome_human.clustering('ATX1_HUMAN')}")
    """

    #example of erdos-renyi with connected component functions
    """
    interactome_random = Interactome(algo="erdos_renyi", proteins=list(map(chr, range(65, 90))), proba=0.1) #proteins = ["A"..."Z"]
    interactome_random.display()
    print(f"Il y a {interactome_random.count_CC()[0]} composantes connexes différentes. Liste des nb de sommets dans chaque: {interactome_random.count_CC()[1]}")
    interactome_random.write_CC()
    """

    #example of barabasi-albert with hist degree
    """
    interactome_scalefree = Interactome(algo="scale_free", proteins=vertices_generator(20))
    interactome_scalefree.display()
    interactome_scalefree.histogram_degree(1, 20)
    """