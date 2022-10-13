import re
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt


SEP = ' |\t' #Separator = space or tab.


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
        """Constructor, inits every attributes in 1 file read
        
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
        for prot1 in self.proteins:
            for prot2 in self.proteins:
                if prot1 == prot2: continue

                if random.random() < q:
                    self.int_list.append((prot1, prot2))
                    self.int_dict[prot1].add(prot2)
                    self.int_dict[prot2].add(prot1)


    def build_from_scalefree(self):
        #start with a 2 nodes clique
        total_deg = 2
        self.int_list.append((self.proteins[0], self.proteins[1]))
        self.int_dict[self.proteins[0]].add(self.proteins[1])
        self.int_dict[self.proteins[1]].add(self.proteins[0])

        for i in range(2, len(self.proteins)):
            for j in range(i):
                # proba =  deg(proteins[j]) / sum(all degrees)
                if random.random() < len(self.int_dict[self.proteins[j]]) / total_deg:
                    self.int_list.append((self.proteins[i], self.proteins[j]))
                    self.int_dict[self.proteins[i]].add(self.proteins[j])
                    self.int_dict[self.proteins[j]].add(self.proteins[i])
                    total_deg += 2



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
        G = nx.DiGraph()
        G.add_edges_from(self.int_list)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=False)
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

    def clustering(self, prot):
        """Computes the clustering coefficient of a protein
        Uses the 2n(prot) / k(k-1) formula with
        n(x) = number of neighbours edges around node x
        k = number of neighbours

        Args:
            prot (str): the protein of which we want the clustering coef
 
        Returns:
            the density of the interactome
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


        



if __name__ == "__main__":
    #print(histogram_degree("bs2/projet_IPP/toy_example.txt", 1, 3))
    #start_time = time.time()
    #clean_interactome("bs2/projet_IPP/Human_HighQuality.txt", "bs2/projet_IPP/Human_HighQualityOut.txt")
    #print("--- %s seconds ---" % (time.time() - start_time))

    interactome1 = Interactome(filename="resources/toy_example.txt")
    interactome1.histogram_degree(1,3)
    print(interactome1.clustering('B'))

    print()
    interactome2 = Interactome(algo="erdos_renyi", proteins=["A", "B", "C", "D", "E", "F"], proba=0.4)
    interactome2.histogram_degree(1,5)
    interactome2.display()
    
    print()
    interactome3 = Interactome(algo="scale_free", proteins=["A", "B", "C", "D", "E", "F"])
    interactome3.histogram_degree(1,5)