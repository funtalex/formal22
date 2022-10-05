import pytest
from src.nfa import NFA
from src.nfa import Edge


@pytest.mark.parametrize('to_state, from_state, word', [('0', '1', ''), ('0', '0', 'a'),
                                                        ('0', '1', 'a'), ('12', '13', 'aba')])
def test_add_edges(to_state, from_state, word):
    nfa = NFA()
    nfa.add_edge(Edge(to_state, from_state, word))
    assert nfa.states == {to_state, from_state}
    assert nfa.sigma == set(word)
    assert nfa.delta[to_state] == {Edge(to_state, from_state, word)}
    nfa.remove_edge(Edge(to_state, from_state, word))
    assert nfa.states == {to_state, from_state}
    assert nfa.sigma == set(word)
    assert nfa.delta[to_state] == set()


@pytest.mark.parametrize('states, term_states, remove_term_states', [([0, 1, 2, 3], [1, 2], [1]), ([2, 3], [0, 1], [4]),
                                                                     ([0, 1], [1, 2], [1, 2]),
                                                                     ([1, 2], [1, 2], [1, 2])])
def test_add_state(states, term_states, remove_term_states):
    nfa = NFA()
    for state in states:
        nfa.add_state(state)
    for state in term_states:
        nfa.add_term(state)
    for state in remove_term_states:
        nfa.remove_term(state)
    assert nfa.states == set(states).union(set(term_states), set(remove_term_states))
    assert nfa.sigma == set()
    assert nfa.terminal == set(term_states).difference(set(remove_term_states))
    for state in nfa.states:
        assert nfa.delta[state] == set()
