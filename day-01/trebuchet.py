from typing import List

def find_first_number(data: str) -> int:
    "Find first character, that is integer. Return character and index"
    
    index = 0
    for char in data:
        if char in [str(i) for i in range(1, 10)]:
            return char, index
        index += 1
        
    else:
        return None, len(data)

def find_solution_of_a(data: str) -> int:
    " Take first and last number in string and join them together "

    fst, _ = find_first_number(data)
    lst, _ = find_first_number(list(reversed(data)))

    return int(fst + lst)

def find_first_last_string_number(data: str, word_list: List[str]):
    """
    Find first number, that is written in string and last.

    Then return numeric value of first word, its index, numeric value of the
    last word and also its index. 
    """
    
    current_min_index = len(data)
    current_min_word = None

    current_max_index = 0
    current_max_word = None

    current_number = 1
    for word in word_list:
        if word in data:
            word_start_index = data.index(word)
            if word_start_index < current_min_index:
                current_min_index = word_start_index
                current_min_word = current_number

            word_last_index = data.rindex(word)
            if word_last_index > current_max_index:
                current_max_index = word_last_index
                current_max_word = current_number

        current_number += 1

    return (str(current_min_word),
            current_min_index,
            str(current_max_word), 
            current_max_index)

def find_solution_of_b(data: str, word_list: List[str]):
    "Also include written integers"

    (min_word,
        min_index,
        max_word, 
        max_index) = find_first_last_string_number(data, word_list)
    
    # Combine also with integers
    fst, fst_index = find_first_number(data)
    lst, lst_index = find_first_number(list(reversed(data)))

    lst_index = len(data) - lst_index - 1

    if fst_index < min_index:
        return_word_1 = fst
    elif fst_index > min_index: 
        return_word_1 = min_word

    if lst_index > max_index:
        return_word_2 = lst
    elif lst_index < max_index:
        return_word_2 = max_word
    else:
        return_word_2 = return_word_1


    final_solution = int(return_word_1 + return_word_2)

    return final_solution


if __name__ == "__main__":

    with open("day-01/input2.txt") as file:
        f = file.read().splitlines()

        ans = sum(find_solution_of_a(ln) for ln in f)

        print(f"Sum of all calibration values: {ans}")

        WORD_LIST = ["one", "two", "three", 
                     "four", "five", "six", 
                     "seven", "eight", "nine"]
        
        ans2 = sum(find_solution_of_b(ln, WORD_LIST) for ln in f)

        print(f"If you also include written numbers: {ans2}")