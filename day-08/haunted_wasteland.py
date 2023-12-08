from typing import List, Tuple, Optional, Dict
import math

class Location:

    def __init__(self,
                 string):
        self.L = string[:3]
        self.R = string[5:8]


def parse_data(data: List[str]) -> Dict[str, Location]:
    return_dict = {}

    for string in data:
        return_dict[string[:3]] = Location(string[7:])

    return return_dict

def find_ZZZ_iter(instructions: str, directions_dict: Dict[str, Location]) -> int:
    """
    Iterate through list and find ZZZ. Return number of steps
    """
    steps = 0
    current_node = "AAA"
    instruction_counter = 0

    while current_node != "ZZZ":
        try:
            direction = instructions[instruction_counter]
            instruction_counter += 1
        except IndexError:
            instruction_counter = 0
            direction = instructions[instruction_counter]
            instruction_counter += 1

        current_node = getattr(directions_dict[current_node], direction)
        steps += 1

    return steps

def final_condition(current_nodes: List[str]) -> bool:
    """ Do all current nodes end with Z """
    for node in current_nodes:
        if node[-1] != "Z":
            return False        
    return True

def make_step(current_nodes: List[str], direction: str, directions_dict: Dict[str, Location]):
    new_list = []

    match direction:
        case "L":
            for node in current_nodes:
                new_list.append(directions_dict[node].L)

        case "R":
            for node in current_nodes:
                new_list.append(directions_dict[node].R)
    
        case _:
            return ValueError("Not a proper direction")
        
    return new_list

def find_ZZZ_simultaniously(instructions: str,
                            directions_dict: Dict[str, Location]) -> int:
    """
    Wrong way, will take more then an hour to calculate.
    """

    steps = 0
    instruction_counter = 0
    current_nodes = []

    for node, _ in directions_dict.items():
        if node[-1] == 'A':
            current_nodes.append(node)

    while not final_condition(current_nodes):
        try:
            direction = instructions[instruction_counter]
            instruction_counter += 1
        except IndexError:
            instruction_counter = 0
            direction = instructions[instruction_counter]
            instruction_counter += 1

        current_nodes = make_step(current_nodes, direction, directions_dict)
        steps += 11

        print(steps)

    return steps

def find_pattern(start_node: str,
                 instructions: str,
                 directions_dict: Dict[str, Location]) -> int:
    """
    Wrong way, will take more then an hour to calculate.
    """

    steps = 0
    instruction_counter = 0
    current_node = start_node

    aux_list = []
    aux_list_steps = []

    while (current_node, instruction_counter) not in aux_list:
        steps += 1

        if final_condition([current_node]):
            aux_list.append((current_node, instruction_counter))
            aux_list_steps.append(steps)

        try:
            direction = instructions[instruction_counter]
            instruction_counter += 1
        except IndexError:
            instruction_counter = 0
            direction = instructions[instruction_counter]
            instruction_counter += 1
        
        current_node = make_step([current_node], direction, directions_dict)[0]

    return aux_list, aux_list_steps

def find_Z_iter(start_node: str, 
                instructions: str,
                directions_dict: Dict[str, Location]) -> int:
    """
    Iterate through list and find ZZZ. Return number of steps and final_node
    """
    steps = 0
    current_node = start_node
    instruction_counter = 0

    while current_node[-1] != "Z":
        try:
            direction = instructions[instruction_counter]
            instruction_counter += 1
        except IndexError:
            instruction_counter = 0
            direction = instructions[instruction_counter]
            instruction_counter += 1

        current_node = getattr(directions_dict[current_node], direction)
        steps += 1

    return steps, current_node

def LCMofArray(a):
  lcm = a[0]
  for i in range(1,len(a)):
    lcm = lcm*a[i]//math.gcd(lcm, a[i])
  return lcm

if __name__ == "__main__":
    with open('day-08/input.txt') as f:
        data = f.read().splitlines()

    instructions = data[0]

    directions_dict = parse_data(data[2:])

    steps = find_ZZZ_iter(instructions, directions_dict)

    print(f"Number of steps needed to reach ZZZ: {steps}")

    periode_dict = {}
    for node, location in directions_dict.items():
        if node[-1] == 'Z':
            pattern = find_pattern(node, instructions, directions_dict)
            periode_dict[node] = pattern[1][1] - 1

    time_until_reach_periode = {}
    for node, location in directions_dict.items():
        if node[-1] == 'A':
            time_until_reach_periode[node] = find_Z_iter(node, instructions, directions_dict)

    # wow, they are the same
    # we just need to find the lcm
    lcm = LCMofArray([val for _,val in periode_dict.items()])
    
    print(f"Steps to simultaniously reach **Z: {lcm}")

    
