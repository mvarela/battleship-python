from board import Board, Orientation, FireResult
from random import choice

class AI:
    def even(self, n):
        return 0 == n % 2

    def odd(self, n):
        return 1 == n % 2

    def checkerboardCoordinates(self):
        """Returns a list of alternating coordinates to target"""
        coords = [(i, j) for i in range(0, self.width)
                  for j in range(0, self.height)
                  if (even(i) and odd(j)) or (odd(i) and even(j))] 

    def adjacents(self, x, y):
        coords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(i, j) for (i, j) in coords
                if (i >= 0) and (x < self.width)
                and (j >= 0) and (j < self.height)]

    def __init__(self, board):
        self.board = board
        self.width = board.width
        self.height = board.height
        self.explored = set()
        self.searchingGlobally = True
        self.remaining = checkerboardCoordinates()
        self.finished = False
        self.stack = []

    def addToLocalSearch(self, x, y):
        adjCoords = [a for a in self.adjacents(x, y)
                     if not(a in self.explored)]
        if len(adjCoords) > 0:
            for a in adjCoords:
                if a in self.remaining:
                    self.remaining.remove(a)
                    self.stack.append(a)
                    self.searchingGlobally = False

    def search(self):
        """Random firing over the remaining checkerboard coordinates"""
        if len(self.remaining) == 0:
            self.finished = True
            return
        elem = (x, y) = choice(self.remaining)
        self.remaining.remove(elem)
        outcome = self.board.fire(x, y)
        self.explored.add(elem)
        if outcome != FireResult.water:
            addToLocalSearch(x, y)

    def handleEmptyStack(self):
        """If the stack becomes empty during the local search, we need
        to go back to a global search, in the same turn"""
        self.searchingGlobally = True
        self.search()

    def localSearch(self):
        """Do a DFS around a cell that is known to be part of a ship"""
        if len(self.stack) == 0:
            self.handleEmptyStack()
            return
        done = False
        while not done:
            try:
                elem = (x, y) = self.stack.pop()
                if not elem in self.explored:
                    done = True
            except IndexError:
                self.handleEmptyStack()
                return
        outcome = self.board.fire(x, y)
        if outcome != FireResult.water:
            addToLocalSearch(x, y)


    def playTurn(self):
        """Plays the next turn. If we don't have a list of likely ship locations, we will
        randomly sample from the not-yet visited positions in the checkerboard pattern. If
        we have hit something, we will perform a local search in the surrounding positions in the grid,
        depth-first"""
        if self.searchingGlobally:
            self.search()
        else:
            self.localSearch()
