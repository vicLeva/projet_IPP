from warnings import filters
import pytest


def is_interaction_file(filename):
    """ with open(filename, 'r') as file:
        file = file.readlines()
        assert int(file[0].rstrip()) 
        assert int(file[0].rstrip()) == len(file)-1, "first line is not the number of interactions"
        for line in file:
            assert line[-1] == "\n"
            assert len(line) == 4 """

is_interaction_file("interactions_test.txt")