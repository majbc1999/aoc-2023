from __future__ import annotations
from typing import List, Tuple, Any


class Galaxy:

    def __init__(self,
                 x: int,
                 y: int,
                 num: int):
        self.x = x
        self.y = y
        self.num = num

    def dist(self, galaxy: Galaxy) -> int:
        return abs(self.x - galaxy.x) + abs(self.y - galaxy.y)
    
    def dist_with_age(self,
                      galaxy: Galaxy,
                      empty_row_list: List[int],
                      empty_col_list: List[int],
                      universe_age: int) -> int:

        age_added = 0
        
        min_x = min(self.x, galaxy.x)
        max_x = max(self.x, galaxy.x)

        for empty_col in empty_col_list:
            if empty_col < max_x and empty_col > min_x:
                age_added += (universe_age - 1)

        min_y = min(self.y, galaxy.y)
        max_y = max(self.y, galaxy.y)

        for empty_row in empty_row_list:
            if empty_row < max_y and empty_row > min_y:
                age_added += (universe_age - 1)

        return self.dist(galaxy) + age_added


def is_empty(data: str):

    for char in data:
        if char == '#':
            return False
    return True

def transpose(lst: List[List[Any]]) -> List[List[Any]]:
    return [[row[i] for row in lst] for i in range(len(lst[0]))]

def expand_universe(data: List[str]) -> List[str]:
    new_data = []
    
    for line in data:
        if is_empty(line):
            new_data.append(line)
        new_data.append(line)

    new_data = transpose(new_data)

    return_data = []

    for line in new_data:
        if is_empty(line):
            return_data.append(line)
        return_data.append(line)
    
    return transpose(return_data)

def empty_rows_and_cols(data: List[str]) -> Tuple[List[int], List[int]]:
    empty_rows = []
    
    for id, row in enumerate(data):
        if is_empty(row):
            empty_rows.append(id)

    data = transpose(data)
    empty_cols = []

    for id, col in enumerate(data):
        if is_empty(col):
            empty_cols.append(id)
        
    return empty_rows, empty_cols


if __name__ == "__main__":
    with open('day-11/input.txt') as f:
        data = f.read().splitlines()

    counter = 0
    universe: List[Galaxy] = []

    for y, line in enumerate(expand_universe(data)):
        for x, char in enumerate(line):
            if char == "#":
                universe.append(
                    Galaxy(x, y, counter)
                )
                counter += 1
        
    sum_ = 0

    for galaxy in universe:
        for galaxy2 in universe:
            sum_ += galaxy.dist(galaxy2)

    print(f"Sum of shortest paths: {sum_ / 2:.0f}")

    old_universe: List[Galaxy] = []

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                old_universe.append(
                    Galaxy(x, y, counter)
                )
                counter += 1

    sum_2 = 0

    empty_row_list, empty_col_list = empty_rows_and_cols(data)

    for galaxy in old_universe:
        for galaxy2 in old_universe:
            sum_2 += galaxy.dist_with_age(galaxy2,
                                          empty_row_list,
                                          empty_col_list,
                                          1000000)
            
    print(f"Sum of lengths of older universe: {sum_2 / 2:.0f}")
