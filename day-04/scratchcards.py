import re
from typing import List, Dict, Optional


class Card:

    index: int
    winning: List[int]
    actual: List[int]
    value: Optional[int]
    new_value: Optional[int]
    
    def __init__(self,
                 index: int,
                 winning: List[int],
                 actual: List[int]):
        self.index = index
        self.winning = winning
        self.actual = actual
        self.value = None
        self.new_value = None

    def return_value(self) -> int:

        if self.value != None:
            return self.value

        points = 0

        for el in self.actual:
            if el in self.winning:
                if points == 0:
                    points = 1
                else:
                    points = points * 2

        self.value = points

        return points

    def return_number_of_matches(self) -> int:
        cntr = 0

        if self.new_value is not None:
            return self.new_value

        for num in self.actual:
            if num in self.winning:
                cntr += 1

        self.new_value = cntr
        return cntr


def parse_cards(data: List[str]) -> List[Card]:
    """
    Parse data into list of objects of class `Card`.
    """

    cards = []
    for line in data:
        regex_exp = r"Card (?P<index>.*): (?P<rest_of>.*)"

        m = re.match(regex_exp, line)
        index = m.groupdict()['index']
        rest_of = m.groupdict()['rest_of']

        winning, actual = rest_of.split('|')
        
        actual = actual.split(' ')
        winning = winning.split(' ')

        new_winning = []
        new_actual = []
        
        for el in winning:
            try:
                new_winning.append(int(el))
            except ValueError:
                continue

        for el in actual:
            try:
                new_actual.append(int(el))
            except ValueError:
                continue

        cards.append(Card(
            index=int(index),
            winning=new_winning,
            actual=new_actual
        ))

    return cards

def number_of_scratchcards(cards: List[Card]) -> int:
    """
    Calculates total value of stack as described in second exercise.
    """
    card_stack_multiplier = {
        card.index: 1 for card in cards
    }

    for card in cards:
        card_specific_multiplier = card_stack_multiplier[card.index]
        card_value = card.return_number_of_matches()

        for index in range(card.index + 1,card.index + card_value + 1):
            if index in card_stack_multiplier.keys():
                card_stack_multiplier[index] += \
                    card_specific_multiplier

    processed = 0
    
    for _, value in card_stack_multiplier.items():
        processed += value

    return processed


with open('day-04/input.txt') as f:
    file = f.read().splitlines()

    cards = parse_cards(file)

    pts = 0
    for card in cards:
        pts += card.return_value()
    
    print(f"Total points from all cards: {pts}")

    total_val = number_of_scratchcards(cards)

    print(f"How many scratchcards {total_val}")

