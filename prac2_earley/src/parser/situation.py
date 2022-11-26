class Situation:
    def __init__(self, from_str, to_left, to_right, index):
        self.from_str = from_str
        self.to_left = to_left
        self.to_right = to_right
        self.index = index

    def __eq__(self, other):
        return self.from_str == other.from_str and self.to_left == other.to_left \
               and self.to_right == other.to_right and self.index == other.index

    def __hash__(self):
        return hash((self.from_str, self.to_left, self.to_right, self.index))
