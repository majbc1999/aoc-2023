from typing import List, Dict, Tuple
import re


class Repetition:
    picks: Dict[str, int]

    def __init__(self, bags):
        self.picks = {}
        self.parse_bags(bags)

    def parse_bags(self, bags: str) -> None:
        bags = bags.split(',')

        regex_string = r"(?P<balls>\d+) (?P<color>.*)"
        for attempt in bags:

            if attempt[0] == ' ':
                attempt = attempt[1:]

            results = re.match(regex_string, attempt).groupdict()

            color = results.get('color')
            balls = results.get('balls')

            if color is not None and balls is not None:
                self.picks[color] = int(balls)

            else:
                raise Exception("Parsing failed")


class Game:
    index: int
    repetitions: List[Repetition]

    def __init__(self,
                 index: int,
                 repetitions: Repetition):
        self.index = index
        self.repetitions = repetitions

    def is_valid(self, valid_dict: Dict[str, int]):
        """
        Is the game valid (a exercise)
        """
        for repetition in self.repetitions:
            for color, value in repetition.picks.items():
                if color in valid_dict.keys():
                    if valid_dict[color] < value:
                        return False
        return True

    def smallest_power(self) -> Dict[str, int]:
        """
        Calculate smallest possible numbers of balls for each repetition
        to be possible (b exercise)
        """
        current_dict = {}

        for repetition in self.repetitions:

            for color, value in repetition.picks.items():
                
                if color not in current_dict:
                    current_dict[color] = value
                else:
                    if current_dict[color] < value:
                        current_dict[color] = value

        power = 1
        for _, value in current_dict.items():
            power = power * value

        return power



def parse_file(data: List[str]) -> List[Game]:
    """
    Parse data to list of games, suitable for the above processor.
    """

    regex_string = r"Game (?P<game_index>\w+): (?P<bags>.*)"
    games = []

    for line in data:
        results = re.match(regex_string, line).groupdict()
        
        index = int(results['game_index'])
        repetitions = []

        bags = results['bags'].split(';')
        for bag in bags:
            repetitions.append(Repetition(
                bag
            ))

        games.append(Game(index, repetitions))

    return games


def max_number_of_each_color(game: List[Tuple[str, int]]) -> Dict[str, int]:
    """
    Game here is represented as list of (color, number of balls).
    """
    values = {}

    for color, n in game:
        if color not in values.keys():
            values[color] = n

        else:
            values[color] = max(values[color], n)

    return values


if __name__ == "__main__":
    with open("day-02/input.txt") as f:
        data = f.read().splitlines()

        games = parse_file(data)

        valid_dict = {
            'red': 12,
            'green': 13,
            'blue': 14
        }

        summed_indices = 0
        summed_power = 0

        for game in games:
            if game.is_valid(valid_dict):
                summed_indices += game.index
            
            summed_power += game.smallest_power()

        print(f"Sum of possible games IDs: {summed_indices}")

        print(f"Sum of power of all games: {summed_power}")