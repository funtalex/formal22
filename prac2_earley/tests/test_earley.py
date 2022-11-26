import pytest
from src.parser.earley import earley
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

rules = dict()
rules['S'] = {Rule('S', 'aSa'), Rule('S', 'bSb'), Rule('S', 'cSc'),
              Rule('S', 'a'), Rule('S', 'b'), Rule('S', 'c'), Rule('S', '')}
non_terminals = set('S')
terminals = set('abc')
start = 'S'
grammar_palindrome = ContextFreeGrammar(non_terminals, terminals, start, rules)


@pytest.mark.parametrize('grammar, word', [(grammar_psp, ''), (grammar_psp, '()'), (grammar_psp, '(()())'),
                                           (grammar_psp, '((()))()()'), (grammar_psp, '(())()()'),
                                           (grammar_word, 'aacb'), (grammar_word, 'aaacbb'),
                                           (grammar_word, 'aaacbb'), (grammar_word, 'aaaaaacbbbbb'),
                                           (grammar_palindrome, 'aaa'), (grammar_palindrome, 'abba'),
                                           (grammar_palindrome, ''), (grammar_palindrome, 'abccba'),
                                           (grammar_palindrome, 'aaabbcbbaaa'), (grammar_palindrome, 'aaabcbacabcbaaa')
                                           ])
def test_contains(grammar, word):
    assert earley(grammar, word)


@pytest.mark.parametrize('grammar, word', [(grammar_psp, '(()()()(((('), (grammar_psp, '))()()('), (grammar_psp, ')('),
                                           (grammar_psp, '()(()('), (grammar_psp, ')()()('),
                                           (grammar_word, ''), (grammar_word, 'bbcaa'), (grammar_word, 'aaaaaabbbbb'),
                                           (grammar_word, 'acaba'), (grammar_word, 'aacaa'),
                                           (grammar_palindrome, 'ab'), (grammar_palindrome, 'abbac'),
                                           (grammar_palindrome, 'aaaaab'), (grammar_palindrome, 'aaabbbaaac'),
                                           (grammar_palindrome, 'aabcbbaa'), (grammar_palindrome, 'bcababcacacaaabba')])
def test_not_contains(grammar, word):
    assert not earley(grammar, word)
