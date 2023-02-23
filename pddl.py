import sys
from expressions import *


dict_pddl_part = {"define" : True, ":requirements" : True, ":types" : True,  ":constants" : True,  ":predicates" : True, ":action" : True, ":parameters" : True, ":precondition" : True, ":effect" : True,
                  ":objects" : True, ":init" : True, ":goal" : True}

def clear_values(line):
    line = line.replace('(',' ( ')
    line = line.replace(')',' ) ')
    line = line.replace('\n',' \n ')
    line = line.replace('\t',' \t ')
    line = line.replace(';',' ; ')
    splitted_line = line.split(" ")
    for x in range(len(splitted_line) -1,-1,-1):
        if splitted_line[x] == "" or splitted_line[x] == "\n" or splitted_line[x] == "\t":
            del splitted_line[x]
    return splitted_line
                

def recursive_list(actual_index, splitted_line):
    sub_list = []
    while(actual_index < len(splitted_line)):
        if(splitted_line[actual_index] == "("):
            actual_index,temp_list = recursive_list(actual_index+1,splitted_line)
            sub_list.append(temp_list)
        elif(splitted_line[actual_index] == ")"):
            return actual_index,sub_list
        else:
            sub_list.append(splitted_line[actual_index])
        actual_index += 1


def part_handle(word):
    try:
        return dict_pddl_part[word]
    except:
        return False
    

def parse_head(file_parsed,head_part):
    head_part.append(")")
    index = 0
    actual_part = ""
    while(index < len(head_part)):
        if(head_part[index] == "("):
            index,sub_list = recursive_list(index+1,head_part)
            for word in sub_list:
                if type(word) == list:
                    for item in word:
                        if part_handle(item):
                            actual_part = item
                            if item not in file_parsed.keys():
                                file_parsed[actual_part] = []
                        elif type(item) == list and actual_part == ":goal":
                                for i in item:
                                    file_parsed[actual_part].append(i)
                        else:
                            file_parsed[actual_part].append(item)
                elif part_handle(word):
                        actual_part = word
                        if word not in file_parsed.keys():
                            file_parsed[actual_part] = []
                else:
                    file_parsed[actual_part].append(word)
        index += 1


def parse_tail(file_parsed,tail_part):
    tail_part.pop()
    index = 0
    actual_action = ""
    actual_part = ""
    file_parsed[":action"] = {}
    just_action = False
    while(index < len(tail_part)):
        if(tail_part[index] == "("):
            index,sub_list = recursive_list(index+1,tail_part)
            for word in sub_list:
                if part_handle(word):
                    if(word == ":action"):
                        just_action = True
                    else:
                        actual_part = word
                        if word not in file_parsed[":action"][actual_action].keys():
                            file_parsed[":action"][actual_action][actual_part] = []
                else:
                    if type(word) == list:
                        for item in word:
                            file_parsed[":action"][actual_action][actual_part].append(item)
                    elif(just_action):
                            actual_action = word
                            file_parsed[":action"][actual_action] = {}
                            just_action = False
                    else:
                        file_parsed[":action"][actual_action][actual_part].append(word)
        index += 1

def parse_dash_list(list):
    result = list
    if '-' in list:
        result = []
        tuple = [[]]
        just_dash = False
        index = 0
        limit = len(list)
        if list[len(list) - 2] == "-":
            limit = len(list) - 1
        while index <= limit:
            if just_dash:
                tuple.append(list[index])
                result.append(tuple)
                tuple = [[]]
                just_dash = False
            elif index == len(list) and tuple[0]:
                tuple.append("") 
                result.append(tuple)
            elif list[index] == "-":
                just_dash = True
            else:
                tuple[0].append(list[index])
            index += 1
    return result

"""
Parses a PDDL domain file contained in the file fname
"""
def parse_domain(fname):
    all_file_list = tokenize(fname)
    file_parsed = {} 

    separator = all_file_list.index(":action")
    head_part = all_file_list[:separator-1]
    tail_part = all_file_list[separator-1:]

    parse_head(file_parsed,head_part)
    parse_tail(file_parsed,tail_part)

    #parse the parameter and types
    for action in file_parsed[":action"]:
        file_parsed[":action"][action][":parameters"] = parse_dash_list(file_parsed[":action"][action][":parameters"])

    file_parsed[":types"] = parse_dash_list(file_parsed[":types"])
    file_parsed[":constants"] = parse_dash_list(file_parsed[":constants"])

    return file_parsed 

"""
Parses a PDDL problem file contained in the file fname
"""  
def parse_problem(fname):
    all_file_list = tokenize(fname)
    file_parsed = {} 
    parse_head(file_parsed,all_file_list)
    #parse objects
    file_parsed[":objects"] = parse_dash_list(file_parsed[":objects"])

    return file_parsed

def tokenize(fname):
    file = open(fname,'r')
    lines = file.readlines()
    all_file_list = []

    for line in lines:
        splitted_line = clear_values(line)
        for word in splitted_line:
            if(word == ';'):
                break
            all_file_list.append(word.lower())
    
    return all_file_list

if __name__ == "__main__":
    print(parse_domain(sys.argv[1]))
    print(parse_problem(sys.argv[2]))
