import pytest
import os
import numpy as np

interactome = pytest.importorskip("Interactome")

def write_example(filename):
    with open(filename, "w") as file:
        file.write(
            """6\nA\tB\nA\tC\nB\tC\nB\tD\nC\tE\nD\tE"""
        )

write_example("/tmp/testFile")
interactome_test = interactome.Interactome("/tmp/testFile")


class Test_Interactome_constructor:
    #DICT
    def test_usual_file_dict(self):
        assert interactome_test.get_int_dict() == {"A":{"B","C"},"B":{"A","C","D"},"C":{"A","B","E"},"D":{"B","E"},"E":{"C","D"}}

    #LIST
    def test_usual_file_list(self):
        assert interactome_test.get_int_list() == [("A","B"),("A","C"),("B","C"),("B","D"),("C","E"),("D","E")]
    

    #PROTEINS
    def test_usual_file_proteins(self):
        assert interactome_test.get_proteins() == ["A", "B", "C", "D", "E"]

    #MATRIX
    #TypeError: 'numpy.ndarray' object is not callable
    """ def test_usual_file_matrix_size(self):
        assert np.size(interactome_test.int_matrix()[0]) == 9
    """


class Test_Interactome_count_vertices:
    def test_usual_file(self):
        assert interactome_test.count_vertices() == 5
    

class Test_Interactome_count_edges:
    def test_usual_file(self):
        assert interactome_test.count_edges() == 6


class Test_Interactome_get_degree:
    def test_usual_file(self):
        assert interactome_test.get_degree("A") == 2


class Test_Interactome_get_max_degree:
    def test_usual_file(self):
        assert interactome_test.get_max_degree() == (["B", "C"], 3)


class Test_Interactome_get_ave_degree:
    def test_usual_file(self):
        assert interactome_test.get_ave_degree() == 2.4


class Test_Interactome_count_degree:
    def test_usual_file(self):
        assert interactome_test.count_degree(2) == 3


class Test_Interactome_histogram_degree:
    def test_usual_file(self):
        assert interactome_test.histogram_degree(1,3) == None

class Test_Interactome_density:
    def test_usual_file(self):
        assert interactome_test.density() == 0.6


class Test_Interactome_clustering:
    def test_usual_file(self):
        assert interactome_test.clustering("A") == 1


os.remove("/tmp/testFile")