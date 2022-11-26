from src.nfa1.nfa1 import NFA1
from src.nfa.nfa import Edge
from queue import Queue
from src.nfa.nfa import EPS


class DFA(NFA1):
    def __init__(self, reg_exp):
        super().__init__(reg_exp)
        new_delta = dict()
        new_terminal = set()
        new_states = set()
        q = Queue()
        q.put(frozenset([self.start]))
        new_states.add(frozenset([self.start]))
        if len(frozenset([self.start]).intersection(self.terminal)) > 0:
            new_terminal.add(frozenset([self.start]))
        while not q.empty():
            cur_state_set = q.get()
            new_delta[cur_state_set] = dict()
            for symbol in self.sigma:
                new_state_set = frozenset([edge.to_state
                                           for cur_state_unit in cur_state_set
                                           for edge in self.delta[cur_state_unit] if edge.word == symbol])
                if len(new_state_set) == 0:
                    continue
                new_delta[cur_state_set][symbol] = Edge(cur_state_set, new_state_set, symbol)
                if new_state_set not in new_states:
                    new_states.add(new_state_set)
                    q.put(new_state_set)
                if len(new_state_set.intersection(self.terminal)) > 0:
                    new_terminal.add(new_state_set)

        self.states = set()
        self.terminal = set()
        self.delta = dict()
        rename_states = dict()
        for state_num, state in enumerate(new_states):
            rename_states[state] = state_num

        for state_num in range(len(rename_states)):
            self.states.add(state_num)
            self.delta[state_num] = dict()
        self.start = rename_states[frozenset([self.start])]
        self.terminal = set([rename_states[x] for x in new_terminal])
        for state in rename_states.keys():
            self.delta[rename_states[state]] = {symbol: Edge(rename_states[state], rename_states[edge.to_state], symbol)
                                                for symbol, edge in new_delta[state].items()}

    def print_doa(self):
        print('DOA: v1')
        print(f'Start: {self.start}')
        print('Acceptance: ', end='')
        for index, value in enumerate(self.terminal):
            print(value, end='')
            if index != len(self.terminal) - 1:
                print(' & ', end='')
        print()

        print('--BEGIN--')
        for state in self.states:
            print(f'State: {state}')
            for symbol in self.delta[state].keys():
                edge = self.delta[state][symbol]
                print(f'-> {edge.word} {edge.to_state}')
        print('--END--')

    def contains(self, word):
        current_state = self.start
        if word == EPS:
            return current_state in self.terminal
        for symbol in word:
            if symbol not in self.delta[current_state].keys():
                return False
            current_state = self.delta[current_state][symbol].to_state
        return current_state in self.terminal
