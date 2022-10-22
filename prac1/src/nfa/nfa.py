from queue import Queue

EPS = ''


class Edge:
    def __init__(self, from_state, to_state, word):
        self.from_state = from_state
        self.to_state = to_state
        self.word = word

    def __eq__(self, other):
        return self.from_state == other.from_state and self.to_state == other.to_state and self.word == other.word

    def __neq__(self, other):
        return self.from_state != other.from_state or self.to_state != other.to_state or self.word != other.word

    def __hash__(self):
        return hash((self.from_state, self.to_state, self.word))


class NFA:

    def __init__(self, reg_exp='0'):
        self.states = set()
        self.delta = dict()
        self.terminal = set()
        self.sigma = set(reg_exp).difference(set('01()*+'))

        if '0' in reg_exp:
            return

        if len(reg_exp) <= 1:
            self.add_state(0)
            self.add_state(1)
            self.terminal = {1}
            self.start = 0
            if reg_exp == '1':
                reg_exp = EPS
            self.add_edge(Edge(0, 1, reg_exp))
            return

        bracket_balance = 0
        for index, symbol in enumerate(reg_exp):
            if symbol == '(':
                bracket_balance += 1
            if symbol == ')':
                bracket_balance -= 1
            if symbol == '+' and bracket_balance == 0:
                nfa_left = NFA(reg_exp[:index])
                nfa_right = NFA(reg_exp[index+1:])
                nfa_left.union(nfa_right)
                self.assign(nfa_left)
                return

        bracket_balance = 0
        for index, symbol in enumerate(reg_exp):
            if symbol == '(':
                bracket_balance += 1
            if symbol == ')':
                bracket_balance -= 1
            if symbol != '*' and bracket_balance == 0 and index < len(reg_exp) - 1 and reg_exp[index + 1] != '*':
                nfa_left = NFA(reg_exp[:index + 1])
                nfa_right = NFA(reg_exp[index+1:])
                nfa_left.concatenate(nfa_right)
                self.assign(nfa_left)
                return

        bracket_balance = 0
        for index, symbol in enumerate(reg_exp):
            if symbol == '(':
                bracket_balance += 1

            if symbol == ')':
                bracket_balance -= 1
            if symbol == '*' and bracket_balance == 0:
                nfa_left = NFA(reg_exp[:index])
                nfa_right = NFA(reg_exp[index + 1:])
                nfa_left.star_klini()
                nfa_left.concatenate(nfa_right)
                self.assign(nfa_left)
                return

        if reg_exp[0] == '(' and reg_exp[-1] == ')':
            nfa = NFA(reg_exp[1:len(reg_exp) - 1])
            self.assign(nfa)

    def assign(self, other):
        self.start = other.start
        self.terminal = other.terminal
        self.states = other.states
        self.delta = other.delta

    def add_state(self, state):
        self.states.add(state)
        self.delta[state] = set()

    def add_edge(self, edge):
        if edge.from_state not in self.states:
            self.states.add(edge.from_state)
        if edge.to_state not in self.states:
            self.states.add(edge.to_state)
        if edge.from_state not in self.delta.keys():
            self.delta[edge.from_state] = set()
        self.sigma.update(set(edge.word))
        self.delta[edge.from_state].add(edge)

    def add_term(self, state):
        if state not in self.states:
            self.add_state(state)
        self.terminal.add(state)

    def remove_term(self, state):
        if state not in self.states:
            self.add_state(state)
        if state in self.terminal:
            self.terminal.remove(state)

    def remove_edge(self, edge):
        self.delta[edge.from_state].remove(edge)

    def union(self, other):
        new_start = len(self.states)
        new_terminal = new_start + 1
        self.add_state(new_start)
        self.add_state(new_terminal)
        shift = len(self.states)
        for state in other.states:
            self.add_state(state + shift)
            for edge in other.delta[state]:
                self.add_edge(Edge(edge.from_state + shift, edge.to_state + shift, edge.word))
        self.add_edge(Edge(new_start, self.start, EPS))
        self.add_edge(Edge(new_start, other.start + shift, EPS))
        self.add_edge(Edge(list(self.terminal)[0], new_terminal, EPS))
        self.add_edge(Edge(list(other.terminal)[0] + shift, new_terminal, EPS))
        self.start = new_start
        self.terminal = {new_terminal}

    def concatenate(self, other):
        shift = len(self.states)
        for state in other.states:
            self.add_state(state + shift)
            for edge in other.delta[state]:
                self.add_edge(Edge(edge.from_state + shift, edge.to_state + shift, edge.word))
        self.add_edge(Edge(list(self.terminal)[0], other.start + shift, EPS))
        self.terminal = {x + shift for x in other.terminal}

    def star_klini(self):
        new_state = len(self.states)
        self.add_state(new_state)
        self.add_edge(Edge(new_state, self.start, EPS))
        self.add_edge(Edge(list(self.terminal)[0], new_state, EPS))
        self.start = new_state
        self.terminal = {new_state}

    def remove_unreachable(self):
        reachable = set()
        q = Queue()
        q.put(self.start)
        while not q.empty():
            cur_state = q.get()
            reachable.add(cur_state)
            for edge in self.delta[cur_state]:
                if edge.to_state not in reachable:
                    q.put(edge.to_state)
        self.states = reachable
        self.terminal = set(x for x in self.terminal if x in reachable)
        self.delta = {state: edges for state, edges in self.delta.items() if state in reachable}

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
            for edge in self.delta[state]:
                if edge.word == EPS:
                    print(f'-> EPS {edge.to_state}')
                else:
                    print(f'-> {edge.word} {edge.to_state}')
        print('--END--')
