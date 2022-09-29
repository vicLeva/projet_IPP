import pytest
import os
import numpy as np

project = pytest.importorskip("project")

def write_example(filename):
    with open(filename, "w") as file:
        file.write(
            """5\nA\tB\nB\tA\nA\tA\nA\tC\nC\tB"""
        )

class Test_read_interaction_file_dict:
    def test_empty_file(self):
        with open("/tmp/testFile", 'w'): pass
        assert project.read_interaction_file_dict("/tmp/testFile") == dict()
        os.remove("/tmp/testFile")

    def test_usual_file(self):
        write_example("/tmp/testFile")
        assert len(project.read_interaction_file_dict("/tmp/testFile")) == 3
        assert project.read_interaction_file_dict("/tmp/testFile") == {"A":{"A","B","C"},
                                                                       "B":{"A","C"},
                                                                       "C":{"A","B"}}
        os.remove("/tmp/testFile")


class Test_read_interaction_file_list:
    def test_empty_file(self):
        with open("/tmp/testFile", 'w'): pass
        assert project.read_interaction_file_list("/tmp/testFile") == list()
        os.remove("/tmp/testFile")

    def test_usual_file(self):
        write_example("/tmp/testFile")
        assert len(project.read_interaction_file_list("/tmp/testFile")) == 5
        assert project.read_interaction_file_list("/tmp/testFile") == [("A","B"),("B","A"),("A","A"),("A","C"),("C","B")]
        os.remove("/tmp/testFile")


class Test_read_interaction_file_mat:
    def test_empty_file(self):
            with open("/tmp/testFile", 'w'): pass
            assert np.size(project.read_interaction_file_mat("/tmp/testFile")[0]) == 0
            assert project.read_interaction_file_mat("/tmp/testFile")[1] == []
            os.remove("/tmp/testFile")

    def test_usual_file_matrix_size(self):
        write_example("/tmp/testFile")
        assert np.size(project.read_interaction_file_mat("/tmp/testFile")[0]) == 9
        os.remove("/tmp/testFile")

    def test_usual_file_matrix_parallel(self):
        write_example("/tmp/testFile")
        matrix = project.read_interaction_file_mat("/tmp/testFile")[0]
        for i in range(3):
            for j in range(3):
                assert matrix[i, j] == matrix[j, i]
        os.remove("/tmp/testFile")

    def test_usual_file_list_content(self):
        write_example("/tmp/testFile")
        vertices_list = project.read_interaction_file_mat("/tmp/testFile")[1]
        assert set(vertices_list) == {"A", "B", "C"}
        os.remove("/tmp/testFile")


class Test_count_vertices:
    def test_empty_file(self):
        with open("/tmp/testFile", 'w'): pass
        assert project.count_vertices("/tmp/testFile") == 0
        os.remove("/tmp/testFile")

    def test_usual_file(self):
        write_example("/tmp/testFile")
        assert project.count_vertices("/tmp/testFile") == 3
        os.remove("/tmp/testFile")


class Test_count_edges:
    def test_empty_file(self):
        with open("/tmp/testFile", 'w'): pass
        assert project.count_edges("/tmp/testFile") == 0
        os.remove("/tmp/testFile")

    def test_usual_file(self):
        write_example("/tmp/testFile")
        assert project.count_edges("/tmp/testFile") == 5
        os.remove("/tmp/testFile")


class Test_clean_interactome:
    def test_usual_file(self):
        write_example("/tmp/testFile")
        project.clean_interactome("/tmp/testFile", "/tmp/testFileOut")
        with open("/tmp/testFileOut", "r") as content:
            for line in content:
                assert line.rstrip() in ("3", "A\tB", "A\tC", "C\tB") 

        os.remove("/tmp/testFile")
        os.remove("/tmp/testFileOut")