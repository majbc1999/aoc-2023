
from typing import List, Dict, Optional

def only_zeros(data: List[int]) -> bool:
    for el in data:
        if el != 0:
            return False
    return True

def generate_all_subseqs(data: List[int]) -> List[List[int]]:
    """
    Return list of all generated subseqs
    """
    subseqs = [data]

    while len(data) >= 2 and not only_zeros(data):
        subseq = []
        for i in range(len(data) - 1):
            subseq.append(data[i + 1] - data[i])
        subseqs.append(subseq)
        data = subseq

    return subseqs

def generate_next_element(data: List[List[int]]) -> int:
    data = reversed(data)
    
    dx = 0
    for i in data:
        dx += i[-1]

    return dx

def generate_previous_element(data: List[List[int]]) -> int:
    data = reversed(data)

    dx = 0
    for i in data:
        dx = i[0] - dx
    
    return dx


with open('day-09/input.txt') as f:
    data = f.read().splitlines()

    seqs = []

    for line in data:
        line = [int(i) for i in line.split(' ')]
        
        seqs.append(generate_all_subseqs(line))

    sum = 0
    for sequence in seqs:
        sum += generate_next_element(sequence)

    print(f"Sum of extrapolated values: {sum}")

    sum_2 = 0
    for sequence in seqs:
        sum_2 += generate_previous_element(sequence)

    print(f"Sum of backwards extrapolated values: {sum_2}")
