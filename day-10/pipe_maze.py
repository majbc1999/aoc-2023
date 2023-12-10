from typing import List, Tuple, Dict
from shapely import Polygon, Point


def find_S(data: List[str]) -> Tuple[int, int]:
    for y, line in enumerate(data):
        if "S" in line:
            return (line.index("S"), y)


def follow_path(data: List[str],
                start_direction: str,
                possible_directions: Dict[str, Dict[str, str]]
                ) -> List[Tuple[int, int]]:
    """
    Follow path and return list of coordinates
    """
    (x, y) = find_S(data)
    S_coords = (x, y)
    direction = start_direction
    visited = [(x, y)]

    while True:
        (x, y) = new_coordinate((x, y), direction)

        if (x, y) == S_coords:
            break

        visited.append((x, y))


        try:
            direction = possible_directions[direction][data[y][x]]
        except Exception:
            raise Exception("Dead end. Choose new `start_direction`")

    return visited


def new_coordinate(current_location: Tuple[int, int],
                   direction: str) -> Tuple[int, int]:
    x, y = current_location
    
    match direction:
        case "up":
            return (x, y - 1)
        case "down":
            return (x, y + 1)
        case "right":
            return (x + 1, y)
        case "left":
            return (x - 1, y)


def draw_output(data: List[str],
                visited: List[Tuple[int, int]],
                output_file: str) -> None:
    """
    Draw the fence.
    """
    with open(output_file, mode='w') as f:
        for y, line in enumerate(data):
            for x, _ in enumerate(line):
                if (x, y) in visited:
                    f.write('O')
                else:
                    f.write(' ')
            f.write('\n')
    return


if __name__ == "__main__":    
    with open('day-10/input.txt') as f:
        data = f.read().splitlines()

    POSSIBLE_DIRECTIONS = {
        "up": {
            "|": "up",
            "7": "left",
            "F": "right"
        },
        "down": {
            "|": "down",
            "L": "right",
            "J": "left"
        },
        "left": {
            "-": "left",
            "L": "up",
            "F": "down"
        },
        "right": {
            "-": "right",
            "7": "down",
            "J": "up"
        },
    }

    directions = ["up", "down", "left", "right"]
    for direction in directions:
        try:
            visited = follow_path(data, direction, POSSIBLE_DIRECTIONS)
        except Exception as e:
            continue

    print(f"Steps for farthest location: {len(visited) / 2:.0f}")

    polygon = Polygon(visited)
    
    inside_counter = 0
    all_points = len(data) * len(data[0])

    for y, line in enumerate(data):
        for x, _ in enumerate(line):
            if (x, y) in visited:
                print(f"Done: {100 * (y * len(data[0]) + x) / all_points}%",
                      end='\r')
                continue
            if polygon.contains(Point(x, y)):
                inside_counter += 1
                print(f"Done: {100 * (y * len(data[0]) + x) / all_points}%",
                      end='\r')

    print(f"Points inside polygon: {inside_counter}")
