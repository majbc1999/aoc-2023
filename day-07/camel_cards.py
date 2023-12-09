from typing import List, Tuple, Union
from collections import Counter
from functools import cmp_to_key


class Hand:
    cards = List[str]
    bid = int

    def __init__(self,
                 cards: Union[str, List[str]],
                 bid: str):
        if isinstance(cards, str):
            self.cards = []
            for card in cards:
                self.cards.append(card)
        else:
            self.cards = cards
        self.bid = int(bid)


def five_of_a_kind(cntr: List[Tuple[str, int]]) -> bool:
    if cntr[0][1] == 5:
        return True
    return False


def four_of_a_kind(cntr: List[Tuple[str, int]]) -> bool:
    if cntr[0][1] == 4:
        return True
    return False


def full_house(cntr: List[Tuple[str, int]]) -> bool:
    if cntr[0][1] == 3 and cntr[1][1] == 2:
        return True
    return False


def three_of_a_kind(cntr: List[Tuple[str, int]]) -> bool:
    if cntr[0][1] == 3 and cntr[1][1] != 2:
        return True
    return False


def two_pair(cntr: List[Tuple[str, int]]) -> bool:
    if cntr[0][1] == 2 and cntr[1][1] == 2:
        return True
    return False


def one_pair(cntr: List[Tuple[str, int]]) -> bool:
    if cntr[0][1] == 2 and cntr[1][1] == 1:
        return True
    return False


def compare(hand_1: Hand, hand_2: Hand) -> int:
    """
    Function, that compares hands and returns 1 if hand_1 wins, 0 for draw and
    -1 in hand_2 wins.
    """
    cntr_1 = Counter(hand_1.cards).most_common(2)
    cntr_2 = Counter(hand_2.cards).most_common(2)

    val_1 = 0
    val_2 = 0

    if five_of_a_kind(cntr_1):
        val_1 = 6
    elif four_of_a_kind(cntr_1):
        val_1 = 5
    elif full_house(cntr_1):
        val_1 = 4
    elif three_of_a_kind(cntr_1):
        val_1 = 3
    elif two_pair(cntr_1):
        val_1 = 2
    elif one_pair(cntr_1):
        val_1 = 1

    if five_of_a_kind(cntr_2):
        val_2 = 6
    elif four_of_a_kind(cntr_2):
        val_2 = 5
    elif full_house(cntr_2):
        val_2 = 4
    elif three_of_a_kind(cntr_2):
        val_2 = 3
    elif two_pair(cntr_2):
        val_2 = 2
    elif one_pair(cntr_2):
        val_2 = 1

    if val_1 > val_2:
        return 1
    elif val_2 > val_1:
        return -1
    else:
        return tie(hand_1, hand_2)


def tie(hand_1: Hand, hand_2: Hand) -> int:
    """
    Return wining comparison in case of basic rules draw
    """
    CARDS = [
        "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"
    ]

    for card1, card2 in zip(hand_1.cards, hand_2.cards):
        if CARDS.index(card1) < CARDS.index(card2):
            return 1
        elif CARDS.index(card1) > CARDS.index(card2):
            return -1

    return 0


def tie_(hand_1: List[str], hand_2: List[str]) -> int:
    CARDS = [
        "A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"
    ]

    for card1, card2 in zip(hand_1, hand_2):
        if CARDS.index(card1) < CARDS.index(card2):
            return 1
        elif CARDS.index(card1) > CARDS.index(card2):
            return -1

    return 0


def all_possible_hands(hand: Hand) -> List[List[str]]:
    """ Returns all possible hands for jokers """

    all_other_cards = [
        "A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"
    ]

    hands = []

    for replacement in all_other_cards:
        new_cards = []
        for card in hand.cards:
            if card == "J":
                new_cards.append(replacement)
            else:
                new_cards.append(card)
        hands.append(new_cards)

    return hands


def max_hand(hand: Hand) -> int:

    all = all_possible_hands(hand)
    max_val = 0
    max_hand = all[0]

    for cards in all:
        cntr_1 = Counter(cards).most_common(2)

        val_1 = 0

        if five_of_a_kind(cntr_1):
            val_1 = 6
        elif four_of_a_kind(cntr_1):
            val_1 = 5
        elif full_house(cntr_1):
            val_1 = 4
        elif three_of_a_kind(cntr_1):
            val_1 = 3
        elif two_pair(cntr_1):
            val_1 = 2
        elif one_pair(cntr_1):
            val_1 = 1

        if val_1 > max_val:
            max_val = val_1
            max_hand = cards
        elif val_1 < max_val:
            continue
        else:
            match tie_(max_hand, cards):
                case -1:
                    max_hand = cards
                case _:
                    continue

    if max_hand.count("A") > 4:
        pass

    return max_hand


def compare_(hand_1_merged: Tuple[Hand, Hand],
             hand_2_merged: Tuple[Hand, Hand]) -> int:

    hand_1, hand_1_original = hand_1_merged
    hand_2, hand_2_original = hand_2_merged

    cntr_1 = Counter(hand_1.cards).most_common(2)
    cntr_2 = Counter(hand_2.cards).most_common(2)

    val_1 = 0
    val_2 = 0

    if five_of_a_kind(cntr_1):
        val_1 = 6
    elif four_of_a_kind(cntr_1):
        val_1 = 5
    elif full_house(cntr_1):
        val_1 = 4
    elif three_of_a_kind(cntr_1):
        val_1 = 3
    elif two_pair(cntr_1):
        val_1 = 2
    elif one_pair(cntr_1):
        val_1 = 1

    if five_of_a_kind(cntr_2):
        val_2 = 6
    elif four_of_a_kind(cntr_2):
        val_2 = 5
    elif full_house(cntr_2):
        val_2 = 4
    elif three_of_a_kind(cntr_2):
        val_2 = 3
    elif two_pair(cntr_2):
        val_2 = 2
    elif one_pair(cntr_2):
        val_2 = 1

    if val_1 > val_2:
        return 1
    elif val_2 > val_1:
        return -1
    else:
        return tie_(hand_1_original.cards, hand_2_original.cards)


with open('day-07/input.txt') as f:
    data = f.read().splitlines()

    cards: List[Hand] = []
    for line in data:
        cards_, bid = line.split(' ')
        cards.append(Hand(cards_, bid))

    sorted_cards = sorted(cards, key=cmp_to_key(compare))

    sum = 0
    for id, card in enumerate(sorted_cards):
        sum += (id + 1) * card.bid
    print(f"Total winnings: {sum}")

    new_cards: List[Hand] = []
    for card in sorted_cards:
        new_cards.append(
            (Hand(
                cards=max_hand(card),
                bid=str(card.bid)),
             card))

    sorted_new_cards = sorted(new_cards, key=cmp_to_key(compare_))

    sum_2 = 0
    for id, card in enumerate(sorted_new_cards):
        sum_2 += (id + 1) * card[1].bid

    print(f"Total winnings with jokers: {sum_2}")
