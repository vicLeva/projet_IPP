import pytest
import os
import numpy as np
import math
import matplotlib.pyplot as plt
import itertools

interactome = pytest.importorskip("Interactome")

def write_example(filename):
    with open(filename, "w") as file:
        file.write(
            """6\nA\tB\nA\tC\nB\tC\nB\tD\nC\tE\nD\tE"""
        )

def write_CC_example(filename):
    with open(filename, "w") as file:
        file.write(
            """4\nA\tB\nA\tC\nD\tE\nF\tG"""
        )

write_example("/tmp/testFile")
interactome_test = interactome.Interactome("/tmp/testFile")

write_CC_example("/tmp/CCtestFile")
interactomeCC_test = interactome.Interactome("/tmp/CCtestFile")

class Test_Interactome_constructor:
    #DICT
    def test_usual_file_dict(self):
        assert interactome_test.get_int_dict() == {"A":{"B","C"},"B":{"A","C","D"},"C":{"A","B","E"},"D":{"B","E"},"E":{"C","D"}}
        assert interactomeCC_test.get_int_dict() == {"A":{"B","C"},"B":{"A"},"C":{"A"},"D":{"E"},"E":{"D"},"F":{"G"},"G":{"F"}}

    #LIST
    def test_usual_file_list(self):
        assert interactome_test.get_int_list() == [("A","B"),("A","C"),("B","C"),("B","D"),("C","E"),("D","E")]
        assert interactomeCC_test.get_int_list() == [("A","B"),("A","C"),("D","E"),("F","G")]


    #PROTEINS
    def test_usual_file_proteins(self):
        assert interactome_test.get_proteins() == ["A", "B", "C", "D", "E"]
        assert interactomeCC_test.get_proteins() == ["A", "B", "C", "D", "E", "F", "G"]

    #MATRIX
    def test_usual_file_matrix_size(self):
        assert interactome_test.int_matrix.shape == (5,5)
    


class Test_Interactome_count_vertices:
    def test_usual_file(self):
        assert interactome_test.count_vertices() == 5
        assert interactomeCC_test.count_vertices() == 7


class Test_Interactome_count_edges:
    def test_usual_file(self):
        assert interactome_test.count_edges() == 6
        assert interactomeCC_test.count_edges() == 4


class Test_Interactome_get_degree:
    def test_usual_file(self):
        assert interactome_test.get_degree("A") == 2
        assert interactomeCC_test.get_degree("E") == 1


class Test_Interactome_get_max_degree:
    def test_usual_file(self):
        assert interactome_test.get_max_degree() == (["B", "C"], 3)
        assert interactomeCC_test.get_max_degree() == (["A"], 2)


class Test_Interactome_get_ave_degree:
    def test_usual_file(self):
        assert interactome_test.get_ave_degree() == 2.4
        assert interactomeCC_test.get_ave_degree() == 8/7


class Test_Interactome_count_degree:
    def test_usual_file(self):
        assert interactome_test.count_degree(2) == 3
        assert interactomeCC_test.count_degree(1) == 6


class Test_Interactome_histogram_degree:
    def test_usual_file(self):
        assert interactome_test.histogram_degree(1,3) == None
        assert interactomeCC_test.histogram_degree(1,2) == None


class Test_Interactome_density:
    def test_usual_file(self):
        assert interactome_test.density() == 0.6
        assert interactomeCC_test.density() == (2*4)/(7*(7-1))


class Test_Interactome_clustering:
    def test_usual_file(self):
        assert interactome_test.clustering("A") == 1
        assert interactomeCC_test.clustering("E") == 0


class Test_Interactome_build_from_random: #on vérifie la moyenne = la clique * la proba ET retrouver la proba sur la normalité
    def test_edges_distribution(self):
        proba = 0.3
        proteins = ["A","B","C","D","E","F","G","H","I","J"]
        len_prot = len(proteins)
        edges_counts = [0] * 100000
        for i in range(100000):
            interactome_random = interactome.Interactome(algo="erdos_renyi", proteins=proteins, proba=proba)
            edges_counts[i] = interactome_random.count_edges()/(len_prot*(len_prot-1)/2) #diviser par la clique ((n*n-1) /2
        """ plt.hist(edges_counts, bins="auto")
        plt.show() """
        assert abs(sum(edges_counts)/len(edges_counts) - proba) < 0.01 

    def test_degree_distribution(self):
        proba = 0.3
        proteins = ["A","B","C","D","E","F","G","H","I","J"]
        max_degree = len(proteins)-1
        degree_counts = [0] * 50000
        for i in range(50000):
            interactome_random = interactome.Interactome(algo="erdos_renyi", proteins = proteins, proba=proba)
            degree_counts[i] = interactome_random.get_ave_degree() 
        """ plt.hist(degree_counts, bins="auto")
        plt.show() """
        assert abs(sum(degree_counts)/len(degree_counts) - (max_degree*proba)) < 0.01
        
class Test_Interactome_build_from_scale_free:
    def test_degree_distribution(self):
        n = 5000
        interactome_random = interactome.Interactome(algo="scale_free", proteins = interactome.vertices_generator(n))
        plt.plot(np.log10(range(5000)), np.log10([interactome_random.count_degree(i) for i in range(n)]), "bo")
        plt.show()

class Test_Interactome_count_CC:
    def test_usual_file(self):
        assert interactome_test.count_CC() == (1, [5])
        assert interactomeCC_test.count_CC() == (3, [3,2,2])


class Test_Interactome_write_CC:
    def test_usual_file(self):
        assert interactome_test.write_CC() == None
        assert interactomeCC_test.write_CC() == None

class Test_Interactome_extract_CC:
    def test_usual_file(self):
        assert set(interactome_test.extract_CC("A")) == {"A","C","B","E","D"}
        assert set(interactomeCC_test.extract_CC("A")) == {"A","C","B"}

class Test_Interactome_compute_CC:
    def test_usual_file(self):
        assert interactome_test.compute_CC() == [1,1,1,1,1]
        assert interactomeCC_test.compute_CC() == [1,1,1,2,2,3,3]




os.remove("/tmp/testFile")
os.remove("/tmp/CCtestFile")