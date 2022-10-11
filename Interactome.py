import re
import numpy as np
import time
import os.path


SEP = ' |\t' #Separator = space or tab.


class Interactome:
    #3.2.3
    def __init__(self, filename): #cleaned file please
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

        #CONSTRUCT MAT
        size = len(self.proteins)
        self.int_matrix = np.zeros((size, size), dtype=int)

        for x, y in self.int_list:
            idx1 = self.proteins.index(x)
            idx2 = self.proteins.index(y)
            self.int_matrix[idx1, idx2] = 1
            self.int_matrix[idx2, idx1] = 1


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

    #3.2.4
    #MEMBER METHODS
    def count_vertices(self):
        return len(self.proteins)

    def count_edges(self):
        return len(self.int_list)

    def get_degree(self, prot):
        return len(self.int_dict[prot])

    def get_max_degree(self):
        max_degree = max(len(int_list) for int_list in self.int_dict.values())
        return [prot for prot, int_list in self.int_dict.items() if len(int_list)==max_degree], \
               max_degree

    def get_ave_degree(self):
        return sum(len(int_list) for int_list in self.int_dict.values()) / len(self.int_dict)

    def count_degree(self, deg):
        return sum(1 for prot in self.int_dict if len(self.int_dict[prot]) == deg)

    def histogram_degree(self, dmin, dmax):
        for i in range(dmin, dmax+1):
            print(i, "*"*self.count_degree(i))

    #3.3.1
    def density(self):
        verts = self.count_vertices()
        edges = self.count_edges()
        return 2*edges / (verts*(verts - 1))

    def clustering(self, prot):
        neighbours = self.int_dict[prot]
        nb_neigh = len(neighbours)

        if nb_neigh <= 1: return 0

        sum_edges = 0
        for n in neighbours:
            for nn in self.int_dict[n]:
                if nn in neighbours:
                    sum_edges += 1
        
        # sum_edges and not 2*sum_edges because we counted every edge twice
        return sum_edges / (nb_neigh * (nb_neigh-1))


        



if __name__ == "__main__":
    #print(histogram_degree("bs2/projet_IPP/toy_example.txt", 1, 3))
    #start_time = time.time()
    #clean_interactome("bs2/projet_IPP/Human_HighQuality.txt", "bs2/projet_IPP/Human_HighQualityOut.txt")
    #print("--- %s seconds ---" % (time.time() - start_time))

    interactome1 = Interactome("resources/toy_example.txt")
    interactome1.histogram_degree(1,3)
    print(interactome1.clustering('B'))
