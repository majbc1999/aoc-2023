
def calculate_distance(delay: int,
                       time_of_race: int) -> int:
    " Distance, that boat travels if we delay for `delay` and race the rest "
    return delay * (time_of_race - delay)

def ways_to_win(time: int,
                record: int) -> int:
    " How many ways there are to beat the time "
   
    for t in range(time):
        if calculate_distance(t, time) > record:
            lowest_time = t
            break

    for t in range(time):
        if calculate_distance(time - t, time) > record:
            highest_time = time - t
            break

    return highest_time - lowest_time + 1


with open('day-06/input.txt') as f:
    data = f.read().splitlines()

    times = data[0].split()[1:]
    distances = data[1].split()[1:]

    times = [int(t) for t in times]
    distances = [int(d) for d in distances]

    counter = 1
    for time, record in zip(times, distances):
        counter *= ways_to_win(time, record)

    print(f"Ways to win: {counter}")

    times = [str(t) for t in times]
    distances = [str(d) for d in distances]

    time = ""
    dist = ""

    for t, d in zip(times, distances):
        time += t
        dist += d

    time = int(time)
    dist = int(dist)

    print(f"Ways to win with kerning: {ways_to_win(time, dist)}")