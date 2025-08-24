class Node:
    def __init__(self, state=None, parent=None, action=None, cost=0, h=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.h = h
        # Depth and children for visualization
        self.depth = 0 if parent is None else parent.depth + 1
        self.children = []

    # Comparison operators for priority queue ordering
    def __lt__(self, other): return (self.h + self.cost) < (other.h + other.cost)
    def __gt__(self, other): return (self.h + self.cost) > (other.h + other.cost)
    def __le__(self, other): return (self.h + self.cost) <= (other.h + other.cost)
    def __ge__(self, other): return (self.h + self.cost) >= (other.h + other.cost)
    def __eq__(self, other): return (self.h + self.cost) == (other.h + other.cost)
    def __ne__(self, other): return (self.h + self.cost) != (other.h + other.cost)
