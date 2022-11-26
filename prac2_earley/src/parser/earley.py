from src.parser.situation import Situation
from src.parser.scan import scan
from src.parser.predict import predict
from src.parser.complete import complete


def earley(grammar, word):
    extra_start = '$'
    derivability = [set() for _ in range(len(word) + 1)]
    new_derivability = {Situation(extra_start, '', grammar.start, 0)}
    prev_size = -1
    derivability[0].update(new_derivability)
    while prev_size != len(derivability[0]):
        prev_size = len(derivability[0])
        prev_derivability = new_derivability
        new_derivability = complete(prev_derivability, derivability)
        new_derivability.update(predict(prev_derivability.union(new_derivability), 0, grammar.rules))
        derivability[0].update(new_derivability)

    for index, letter in enumerate(word):
        new_derivability = scan(derivability[index], letter)
        prev_size = -1
        derivability[index + 1].update(new_derivability)
        while prev_size != len(derivability[index + 1]):
            prev_size = len(derivability[index + 1])
            prev_derivability = new_derivability
            new_derivability = complete(prev_derivability, derivability)
            new_derivability.update(predict(prev_derivability.union(new_derivability), index + 1, grammar.rules))
            derivability[index + 1].update(new_derivability)

    return Situation(extra_start, grammar.start, '', 0) in derivability[len(word)]
