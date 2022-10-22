from src.dfa.dfa import DFA
from src.nfa.nfa import Edge


class FDFA(DFA):
    def __init__(self, reg_exp):
        super().__init__(reg_exp)
        stock = len(self.states)
        was_full = True
        for state in self.states:
            for symbol in self.sigma:
                if symbol not in self.delta[state].keys():
                    was_full = False
                    self.delta[state][symbol] = Edge(state, stock, symbol)
        if not was_full:
            self.states.add(stock)
            self.delta[stock] = dict()
            for symbol in self.sigma:
                self.delta[stock][symbol] = Edge(stock, stock, symbol)
