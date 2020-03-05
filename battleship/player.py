class Player:
    def __init__(self, ownBoard, opponentBoard, freeShips):
        self.ownBoard = ownBoard
        self.opponentBoard = opponentBoard
        self.freeShips = freeShips
        self.readyToPlay = False

    def populateBoard(self):
      """ Automatically assigns remaining pieces to the board """
      if len(self.freeShips) > 0:
          self.ownBoard.populate(self.freeShips)
          self.freeShips = []
          self.readyToPlay = True

    def addShip(self, x, y, length, orientation):
        if length in self.freeShips and self.ownBoard.canAdd(x, y, length, orientation):
            self.ownBoard.addShip(x, y, length, orientation)
            self.freeShips.remove(length)
            if len(self.freeShips) == 0:
                self.readyToPlay = True 
            return True
        else:
            return False

    def fire(self, x, y):
        return self.opponentBoard.fire(x, y)
