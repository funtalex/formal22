from src.nfa import Edge
from src.nfa import NFA


class NFA01(NFA):
    def __init__(self, reg_exp):
        super().__init__(reg_exp)
        old_delta = self.delta
        for state, edges in old_delta.items():
            for edge in edges:
                if len(edge.word) > 1:
                    for symbol in edge.word:
                        self.add_edge(Edge(state, edge.to_state, symbol))
                    self.remove_edge(edge)
