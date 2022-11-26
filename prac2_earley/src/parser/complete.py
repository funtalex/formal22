from src.parser.situation import Situation


def complete(derivability, derivability_array):
    result = set()
    for first_situation in derivability:
        if first_situation.to_right != '':
            continue
        for second_situation in derivability_array[first_situation.index]:
            if len(second_situation.to_right) > 0 \
                    and second_situation.to_right[0] == first_situation.from_str:
                result.add(Situation(second_situation.from_str,
                                     second_situation.to_left + first_situation.from_str,
                                     second_situation.to_right[1:], second_situation.index))
    return result
