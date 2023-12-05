from typing import List, Dict, Optional, Tuple


def parse_file_to_dicts(data: List[str]):
    """
    Parse the input file to many dicts in order to queue easier
    """

    seed_to_soil = {}
    soil_to_fer = {}
    fer_to_wat = {}
    wat_to_lig = {}
    lig_to_temp = {}
    temp_to_hum = {}
    hum_to_loc = {}

    for index, line in enumerate(data):
        try:
            match line[:5]:
                case "seeds":
                    pass
                case "seed-":
                    seed_startpoint = index
                case "soil-":
                    soil_startpoint = index
                case "ferti":
                    ferti_startpoint = index
                case "water":
                    water_startpoint = index
                case "light":
                    light_startpoint = index
                case "tempe":
                    tempe_startpoint = index
                case "humid":
                    humid_startpoint = index
                case _:
                    continue
        except ValueError:
            continue

    seeds =  data[0][7:].split(' ')

    seeds = [int(seed) for seed in seeds]

    seed_to_soil = {}
    soil_to_fer = {}
    fer_to_wat = {}
    wat_to_lig = {}
    lig_to_temp = {}
    temp_to_hum = {}
    hum_to_loc = {}

    seed_to_soil = parse_lines_to_dict(seed_to_soil,
                                       lines[seed_startpoint+1:soil_startpoint-1])
    soil_to_fer = parse_lines_to_dict(soil_to_fer,
                                      lines[soil_startpoint+1:ferti_startpoint-1])
    fer_to_wat = parse_lines_to_dict(fer_to_wat,
                                     lines[ferti_startpoint+1:water_startpoint-1])
    wat_to_lig = parse_lines_to_dict(wat_to_lig,
                                     lines[water_startpoint+1:light_startpoint-1])
    lig_to_temp = parse_lines_to_dict(lig_to_temp,
                                      lines[light_startpoint+1:tempe_startpoint-1])
    temp_to_hum = parse_lines_to_dict(temp_to_hum,
                                      lines[tempe_startpoint+1:humid_startpoint-1])
    hum_to_loc = parse_lines_to_dict(hum_to_loc,
                                     lines[humid_startpoint+1:])
    
    return (seeds, seed_to_soil, soil_to_fer, fer_to_wat, wat_to_lig, lig_to_temp, temp_to_hum, hum_to_loc)

def parse_lines_to_dict(dictionary: Dict[int, Tuple[int, int]],
                        lines: List[str]) -> Dict[int, Tuple[int, int]]:
    """
    Parse line to dictionary
    """
    for line in lines:
        start_val, start_key, step = line.split(' ')

        dictionary[int(start_key)] = (int(start_val), int(step))

    return dictionary

def query_seed_location(seed_n: int, 
                        seed_to_soil: Dict[int, int], 
                        soil_to_fer: Dict[int, int], 
                        fer_to_wat: Dict[int, int], 
                        wat_to_lig: Dict[int, int], 
                        lig_to_temp: Dict[int, int], 
                        temp_to_hum: Dict[int, int], 
                        hum_to_loc: Dict[int, int]):
    """
    Query seed location from dictionaries
    """
    soil = get_source(seed_n, seed_to_soil)
    fer = get_source(soil, soil_to_fer)
    wat = get_source(fer, fer_to_wat)
    lig = get_source(wat, wat_to_lig)
    temp = get_source(lig, lig_to_temp)
    hum = get_source(temp, temp_to_hum)
    return get_source(hum, hum_to_loc)

def get_source(n: int,
               dictionary: Dict[int, Tuple[int, int]]) -> int:
    for start_key, (start_val, step)  in dictionary.items():
        if n >= start_key and n <= start_key + step:
            return start_val + (n - start_key)

    return n

def modify_seeds(seed_list: List[int]) -> List[int]:
    new_seed_list = []

    for i in range(len(seed_list) // 2):
        seed_n = seed_list[2*i]
        seed_range = seed_list[2*i + 1]
        new_seed_list.append((seed_n, seed_range))

    return new_seed_list

def reverse_dict(dictionary: Dict[int, Tuple[int, int]]):
    new_dict = {}

    for key, (val, step) in dictionary.items():
        new_dict[val] = (key, step)
    
    return new_dict

def query_seed_from_location(location: int, 
                             rev_seed_to_soil: Dict[int, int], 
                             rev_soil_to_fer: Dict[int, int], 
                             rev_fer_to_wat: Dict[int, int], 
                             rev_wat_to_lig: Dict[int, int], 
                             rev_lig_to_temp: Dict[int, int], 
                             rev_temp_to_hum: Dict[int, int], 
                             rev_hum_to_loc: Dict[int, int]):
    
    """
    Query seed location from dictionaries
    """
    hum = get_source(location, rev_hum_to_loc)
    temp = get_source(hum, rev_temp_to_hum)
    lig = get_source(temp, rev_lig_to_temp)
    wat = get_source(lig, rev_wat_to_lig)
    fer = get_source(wat, rev_fer_to_wat)
    soil = get_source(fer, rev_soil_to_fer)
    return get_source(soil, rev_seed_to_soil)


if __name__ == "__main__":
    with open('day-05/input.txt') as f:
        lines = f.read().splitlines()

    (seeds, seed_to_soil, soil_to_fer, fer_to_wat, wat_to_lig, lig_to_temp, temp_to_hum, hum_to_loc) = \
        parse_file_to_dicts(lines)
    
    locations: List[int] = []
    for seed in seeds:
        locations.append(query_seed_location(seed,
                                             seed_to_soil,
                                             soil_to_fer,
                                             fer_to_wat,
                                             wat_to_lig,
                                             lig_to_temp,
                                             temp_to_hum,
                                             hum_to_loc))

    print(f"Minimal location, that corresponds to seed is: {min(locations)}")

    rev_seed_to_soil = reverse_dict(seed_to_soil)
    rev_soil_to_fer = reverse_dict(soil_to_fer)
    rev_fer_to_wat = reverse_dict(fer_to_wat)
    rev_wat_to_lig = reverse_dict(wat_to_lig)
    rev_lig_to_temp = reverse_dict(lig_to_temp)
    rev_temp_to_hum = reverse_dict(temp_to_hum)
    rev_hum_to_loc = reverse_dict(hum_to_loc)

    new_seeds = modify_seeds(seeds)
    end = False
    
    for loc in range(max(locations)):
        seed_n = query_seed_from_location(loc,
                                          rev_seed_to_soil,
                                          rev_soil_to_fer,
                                          rev_fer_to_wat,
                                          rev_wat_to_lig,
                                          rev_lig_to_temp,
                                          rev_temp_to_hum,
                                          rev_hum_to_loc)
        
        for (lkp_seed, lkp_range) in new_seeds:
            if seed_n >= lkp_seed and seed_n <= lkp_seed + lkp_range:
                end = True
                break

        if end:
            print(f"Minimal location for modified seeds: {loc}")
            break
