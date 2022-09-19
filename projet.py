import re

def read_interaction_file_dict(filename):
    dic = dict()
    with open(filename) as content:
        content.readline() #skip 1st line
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())
            if split[0] in dic:
                dic[split[0]].append(split[1])
            else:
                dic[split[0]] = [split[1]]
    return dic

def read_interaction_file_list(filename):
    with open(filename) as content:
        interaction_list = [0] * int(content.readline())
        index = 0
        for line in content.readlines():
            split = re.split(' |\t', line.rstrip())
            interaction_list[index] = tuple(split)
            index += 1
       
    return interaction_list

print(read_interaction_file_list("toy_example.txt"))
#print(read_interaction_file_dict("Human_HighQuality.txt"))