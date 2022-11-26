import pytest
from src.nfa.nfa import NFA
from src.dfa.dfa import DFA
from src.mfdfa.mfdfa import MFDFA


@pytest.mark.parametrize('reg_exp', ['(a+b)*b(a+1)b(a+b)*', 'ac(a+b)*+b*ac'])
def test_print(reg_exp):
    nfa = NFA(reg_exp)
    dfa = DFA(reg_exp)
    mfdfa = MFDFA(reg_exp)
    nfa.print_doa()
    dfa.print_doa()
    mfdfa.print_doa()
