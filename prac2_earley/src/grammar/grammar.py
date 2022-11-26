class ContextFreeGrammar:
    def __init__(self, non_terminals, terminals, start, rules):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start = start
        self.rules = rules
