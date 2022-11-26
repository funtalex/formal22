import pytest
from src.dfa.dfa import DFA
from src.mfdfa.mfdfa import MFDFA


@pytest.mark.parametrize('reg_exp, words', [('(a+b)*b(a+1)b(a+b)*', ['bb', 'abbba', 'bbababaa', 'bba']),
                                            ('a', ['a']), ('1', ['']), ('a+b*', ['a', 'bbbbb', 'bbb', '']),
                                            ('ac(a+b)*+b*ca', ['ac', 'aca', 'bbbca', 'acbbab', 'ca'])])
def test_contains(reg_exp, words):
    dfa = DFA(reg_exp)
    mfdfa = MFDFA(reg_exp)
    for word in words:
        assert dfa.contains(word)
        assert mfdfa.contains(word)


@pytest.mark.parametrize('reg_exp, words', [('(a+b)*b(a+1)b(a+b)*', ['a', '', 'aabaa', 'baaa']),
                                            ('a', ['b', 'ab', 'ba', '']), ('1', ['a', 'ab', 'b']),
                                            ('a+b*', ['bbaa', 'aaa', 'abba']),
                                            ('ac(a+b)*+b*ac', ['', 'a', 'aaa', 'bbca', 'acac'])])
def test_not_contains(reg_exp, words):
    dfa = DFA(reg_exp)
    mfdfa = MFDFA(reg_exp)
    for word in words:
        assert not dfa.contains(word)
        assert not mfdfa.contains(word)
