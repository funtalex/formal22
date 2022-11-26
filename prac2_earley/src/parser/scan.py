from src.parser.situation import Situation


def scan(derivability, letter):
    result = set()
    for situation in derivability:
        if len(situation.to_right) > 0 and situation.to_right[0] == letter:
            result.add(
                Situation(situation.from_str, situation.to_left + letter, situation.to_right[1:], situation.index))
    return result
