import pytest
from src.parser.cyk import cyk
from src.grammar.rules import Rule
from src.grammar.grammar import ContextFreeGrammar

rules = dict()
rules['A'] = {Rule('A', ''), Rule('A', 'BB'), Rule('A', 'CD')}
rules['B'] = {Rule('B', 'CD'), Rule('B', 'BB')}
rules['C'] = {Rule('C', '(')}
rules['D'] = {Rule('D', 'BE'), Rule('D', ')')}
rules['E'] = {Rule('E', ')')}

non_terminals = set('ABCDE')
terminals = set('()')
start = 'A'

grammar_psp = ContextFreeGrammar(non_terminals, terminals, start, rules)

rules = dict()
rules['S'] = {Rule('S', 'AC')}
rules['D'] = {Rule('D', 'CB')}
rules['C'] = {Rule('C', 'AD'), Rule('C', 'c')}
rules['B'] = {Rule('B', 'b')}
rules['A'] = {Rule('A', 'a')}

non_terminals = set('SABCD')
terminals = set('abc')
start = 'S'

grammar_word = ContextFreeGrammar(non_terminals, terminals, start, rules)


@pytest.mark.parametrize('grammar, word', [(grammar_psp, ''), (grammar_psp, '()'), (grammar_psp, '(()())'),
                                           (grammar_psp, '((()))()()'), (grammar_psp, '(())()()'),
                                           (grammar_word, 'aacb'), (grammar_word, 'aaacbb'),
                                           (grammar_word, 'aaacbb'), (grammar_word, 'aaaaaacbbbbb')])
def test_contains(grammar, word):
    assert cyk(grammar, word)


@pytest.mark.parametrize('grammar, word', [(grammar_psp, '(()()()(((('), (grammar_psp, '))()()('), (grammar_psp, ')('),
                                           (grammar_psp, '()(()('), (grammar_psp, ')()()('),
                                           (grammar_word, ''), (grammar_word, 'bbcaa'), (grammar_word, 'aaaaaabbbbb'),
                                           (grammar_word, 'acaba'), (grammar_word, 'aacaa')])
def test_contains(grammar, word):
    assert not cyk(grammar, word)
