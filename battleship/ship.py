class Ship:
    def __init__(self, length):
        self.length = length
        self.hits = set()

    def hit(index):
        """ Register a hit at position `index`"""
        if index <= length:
            self.hits.add(index)

    def isSunk():
        """True if the ship is sunk"""
        return len(self.hits) == self.length
