from src.nfa.nfa import EPS
from src.nfa.nfa import Edge
from src.nfa01.nfa01 import NFA01


class NFA1(NFA01):
    def __init__(self, reg_exp):
        super().__init__(reg_exp)

        old_delta = self.delta
        epsilon_closure = dict()
        for state, edges in old_delta.items():
            epsilon_closure[state] = set()
            for edge in edges:
                if edge.word == EPS:
                    epsilon_closure[state].add(edge.to_state)

        for step in range(len(self.states)):
            old_epsilon_closure = epsilon_closure
            for state, edges in old_delta.items():
                for edge in edges:
                    if edge.word == EPS:
                        epsilon_closure[state].update(old_epsilon_closure[edge.to_state])

        for state, delta_eps_dict in epsilon_closure.items():
            for delta_eps in delta_eps_dict:
                for edge in old_delta[delta_eps]:
                    if edge.word != EPS:
                        self.delta[state].add(Edge(state, edge.to_state, edge.word))

        new_terminal = self.terminal
        for state, delta_eps_dict in epsilon_closure.items():
            new_terminal.update(set(state for term_state in delta_eps_dict if term_state in self.terminal))
        self.terminal = new_terminal

        for state in self.delta.keys():
            self.delta[state] = set([edge for edge in self.delta[state] if edge.word != EPS])

        self.remove_unreachable()
