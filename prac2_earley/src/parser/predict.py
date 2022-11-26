from src.parser.situation import Situation


def predict(derivability, index, rules):
    result = set()
    for situation in derivability:
        if len(situation.to_right) > 0 and situation.to_right[0].isupper():
            for rule in rules[situation.to_right[0]]:
                result.add(Situation(rule.left, '', rule.right, index))
    return result
