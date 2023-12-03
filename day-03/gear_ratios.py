from typing import List, Tuple

class Number:
    num: int
    line_index: int
    start_char_index: int
    end_char_index: int

    def __init__(self,
                 num,
                 line_index,
                 start_char_index,
                 end_char_index):
        self.num = num
        self.line_index = line_index
        self.start_char_index = start_char_index
        self.end_char_index = end_char_index

    def all_adjacent_coords(self):
        crds: List[Tuple[int, int]] = []

        for i in range(self.start_char_index - 1, self.end_char_index + 2):
            crds.append((self.line_index - 1, i))
            crds.append((self.line_index + 1, i))

        crds.append((self.line_index, self.start_char_index - 1))
        crds.append((self.line_index, self.end_char_index + 1))

        return crds


def extract_numbers(data: List[str]) -> List[Number]:
    """
    Extract `Number` objects from data
    """

    already_visited_indices: List[Tuple[int, int]] = []
    all_numbers: List[Number] = []

    for line_index, line in enumerate(data):
        for char_index, char in enumerate(line):
            if (line_index, char_index) not in already_visited_indices:
                already_visited_indices.append((line_index, char_index))

                if char.isnumeric():
                    number = char
                    number_start_index = char_index
                    for next_char_id, next_char in enumerate(line[(char_index + 1):]):
                        already_visited_indices.append((line_index,
                                                        char_index + 1 + next_char_id))
                        if next_char.isnumeric():
                            number += next_char
                            number_end_index = char_index + 1 + next_char_id
                        else:
                            number_end_index = char_index + next_char_id
                            break

                    all_numbers.append(Number(
                        num=int(number),
                        line_index=line_index,
                        start_char_index=number_start_index,
                        end_char_index=number_end_index
                    ))
                    
    return all_numbers

def is_symbol_adjacent(number: Number,
                       data: List[str],
                       symbol_list: List[str]) -> bool:
    """
    Checks is any symbol from `symbol_list` is adjacent to `number` in `data`.
    """

    line_indices = [number.line_index - 1,
                    number.line_index + 1]
    
    char_indices = list(range(number.start_char_index - 1,
                              number.end_char_index + 2))

    for line_index in line_indices:
        for char_index in char_indices:
            try:
                cur_char = data[line_index][char_index]
                if cur_char in symbol_list:
                    return True
            except IndexError:
                continue

    try:
        cur_char = data[number.line_index][number.start_char_index - 1]
        if cur_char in symbol_list:
            return True
                
    except IndexError:
        pass

    try:
        cur_char = data[number.line_index][number.end_char_index + 1]
        if cur_char in symbol_list:
            return True
                
    except IndexError:
        pass

    return False

def find_all_symbols_in_data(data: List[str]):
    symbol_list: List[str] = []

    for line in data:
        for char in line:
            if not char.isnumeric() and char != '.':
                symbol_list.append(char)

    return list(set(symbol_list))

def find_gear_ratio(location: Tuple[int, int], numbers: List[Number]) -> int:
    """
    Find a ration of gear, located at `location`.
    """

    ratio = 1
    adjacent_count = 0

    for number in numbers:
        if location in number.all_adjacent_coords():
            ratio = ratio * number.num
            adjacent_count += 1

    if adjacent_count == 2:
        return ratio
    else:
        return 0

def extract_gears(data: List[str]) -> List[Tuple[int, int]]:
    """
    Extract coordinates of all gears.
    """
    coords: List[Tuple[int, int]] = []

    for line_id, line in enumerate(data):
        for char_id, char in enumerate(line):
            if char == '*':
                coords.append((line_id, char_id))

    return coords

def find_ratios_of_gears(data: List[str], numbers: List[Number]) -> int:
    """
    Find ratio of each gear and return a sum
    """
    gears = extract_gears(data)
    ratio_sum = 0

    for gear_coord in gears:
        ratio_sum += find_gear_ratio(gear_coord, numbers)

    return ratio_sum


if __name__ == "__main__":
    with open('day-03/input.txt') as f:
        data = f.read().splitlines()

        sum_of_engine_schematics = 0

        numbers = extract_numbers(data)
        symbol_list = find_all_symbols_in_data(data)

        for number in numbers:
            if is_symbol_adjacent(number, data, symbol_list):
                sum_of_engine_schematics += number.num

        print("Sum of all numbers in engine schematics: "
            f"{sum_of_engine_schematics}")
        
        gears_ratio_sum = find_ratios_of_gears(data, numbers)

        print(f"Sum of all gear ratios in schematics: {gears_ratio_sum}")
