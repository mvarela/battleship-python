class Ship:
    def __init__(self, length):
        self.length = length
        self.hits = set()

    def hit(self, index):
        """ Register a hit at position `index`"""
        if index <= self.length:
            self.hits.add(index)

    def isSunk(self):
        """True if the ship is sunk"""
        return len(self.hits) == self.length
