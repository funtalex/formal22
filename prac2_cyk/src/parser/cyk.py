from src.grammar.rules import Rule


def cyk(grammar, word):
    if word == '':
        return Rule(grammar.start, '') in grammar.rules[grammar.start]

    derivability = {key: [[False for start in range(len(word) + 1)] for finish in range(len(word) + 1)]
                    for key in grammar.non_terminals}

    for index, letter in enumerate(word):
        for non_term in grammar.non_terminals:
            if Rule(non_term, letter) in grammar.rules[non_term]:
                derivability[non_term][index][index + 1] = True

    for word_length in range(2, len(word) + 1):
        for start in range(0, len(word) + 1 - word_length):
            finish = start + word_length
            for non_term in grammar.non_terminals:
                for rule in grammar.rules[non_term]:
                    if len(rule.right) < 2:
                        continue
                    for mid in range(start, finish):
                        derivability[non_term][start][finish] |= \
                            derivability[rule.right[0]][start][mid] & \
                            derivability[rule.right[1]][mid][finish]

    return derivability[grammar.start][0][len(word)]
