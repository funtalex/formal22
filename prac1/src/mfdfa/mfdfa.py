from src.nfa.nfa import Edge
from src.fdfa.fdfa import FDFA


class MFDFA(FDFA):
    def __init__(self, reg_exp):
        if isinstance(reg_exp, str):
            super().__init__(reg_exp)
        else:
            self.assign(reg_exp)
            self.sigma = reg_exp.sigma
        next_eq_classes = dict()
        next_cnt_classes = 2
        for state in self.states:
            if state in self.terminal:
                next_eq_classes[state] = 0
            else:
                next_eq_classes[state] = 1

        prev_eq_classes = dict()
        prev_cnt_classes = -1
        members_of_classes = dict()

        while prev_cnt_classes != next_cnt_classes:
            prev_eq_classes = next_eq_classes.copy()
            prev_cnt_classes = next_cnt_classes
            next_cnt_classes = 0
            members_of_classes = dict()
            for state in self.states:
                member_of_class = [prev_eq_classes[state]]
                for symbol in self.sigma:
                    member_of_class.append(prev_eq_classes[self.delta[state][symbol].to_state])
                member_of_class = tuple(member_of_class)
                if member_of_class in members_of_classes.keys():
                    next_eq_classes[state] = members_of_classes[member_of_class]
                else:
                    next_eq_classes[state] = next_cnt_classes
                    members_of_classes[member_of_class] = next_cnt_classes
                    next_cnt_classes += 1

        new_delta = dict()
        for state in self.states:
            new_delta[next_eq_classes[state]] = dict()
            for symbol in self.sigma:
                new_delta[next_eq_classes[state]][symbol] = Edge(next_eq_classes[state],
                                                                 next_eq_classes[self.delta[state][symbol].to_state],
                                                                 symbol)
        self.delta = new_delta
        self.start = next_eq_classes[self.start]
        self.states = set(x for x in range(next_cnt_classes))
        self.terminal = set(next_eq_classes[state] for state in self.terminal)
