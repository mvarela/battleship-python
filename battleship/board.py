from pieces import (EmptyPiece, WaterPiece,
             ShipPiece, HitShipPiece)
from enum import Enum
from random import choice, randint
from ship import Ship
from uuid import uuid4


class Orientation(Enum):
   horizontal = 0
   vertical = 1

class FireResult(Enum):
    water = 0
    hit = 1
    sunk = 2

class Board:
  """Represents the core of our data model: a rectangular grid where we can
position ships, fire upon them, and check the status of a grid cell that has
been fired upon.

  """
  def __init__(self, width, height):
    self.height = height
    self.width = width
    self.grid = [[EmptyPiece() for y in range(height)] for x in range(width)]
    self.ships = {}

  def rowString(self, n, opponentView = False):
    if n <= self.height:
      rowStr = ' | '.join([self.grid[i][n].draw(opponentView) for i in range(self.width)])
      return('| ' + rowStr + ' |\n')
    else:
      return ''

  def printBoard(self, opponentView = False):
    rows = [self.rowString(i, opponentView) for i in range(self.height)]
    header = '  ' + '| '  + ' | '.join(['%s' %i for i in range(0,self.width)]) + ' |'
    hsep =  ''.join(['_' for i in range(0, len(header))]) + '\n'
    print(header)
    print(hsep)
    for idx, r in enumerate(rows):
      # we ommit the index string padding for simplicity, since it'll be <10 in the game
      print(str(idx) + ' ' +r)

  def positions(self, x, y, length, orientation):
     """Auxiliary function to return the coordinates occupied by adding a ship"""
     if x < 0 or y < 0:
        return False
     xEnd = x
     yEnd = y
     if(orientation == Orientation.horizontal):
        xEnd = x + length
     else:
        yEnd = y + length
  
     if xEnd >= self.width or yEnd >= self.height:
         return False
     else:
        if orientation == Orientation.horizontal:
           return [(i,y) for i in range(x, xEnd)]
        else:
           return [(x,j) for j in range(y, yEnd)]
  
  def canAdd(self, x, y, length, orientation):
     positions = self.positions(x, y, length, orientation)
     if positions:
        cells = [self.grid[x][y].isEmpty() for (x,y) in positions]
        return all(cells)
     else:
        return False

  def addShip(self, x, y, length, orientation):
      if self.canAdd(x, y, length, orientation):
          ship = Ship(length)
          coords = self.positions(x, y, length, orientation)
          id = uuid4()
          self.ships[id] = ship
          for idx, (i, j) in enumerate(coords):
              self.grid[i][j] = ShipPiece(id, idx)
          return True
      else:
          return False

  def fire(self,x,y):
      result = FireResult.water
      if x < self.width and y < self.height:
          piece = self.grid[x][y]
          if piece.isEmpty():
              self.grid[x][y] = WaterPiece()
          else:
              idx = piece.index
              shipId = piece.shipId
              self.ships[shipId].hit(idx)
              self.grid[x][y] = HitShipPiece(shipId, idx)
              result = FireResult.hit
              if self.ships[shipId].isSunk():
                  result = FireResult.sunk
      return result
  

  def populate(self, sizes):
      for s in sizes:
          done = False
          while not done:
              orientation = choice(list(Orientation))
              maxX = self.width - 1 if orientation == Orientation.vertical else self.width - s
              maxY = self.height - 1 if orientation == Orientation.horizontal else self.height - s
              x = randint(0, maxX)
              y = randint(0, maxY)
              if self.canAdd(x, y, s, orientation):
                  self.addShip(x, y, s, orientation)
                  done = True
  def populate(self, sizes):
      for s in sizes:
          done = False
          while not done:
              orientation = choice(list(Orientation))
              maxX = self.width - 1 if orientation == Orientation.vertical else self.width - s
              maxY = self.height - 1 if orientation == Orientation.horizontal else self.height - s
              x = randint(0, maxX)
              y = randint(0, maxY)
              if self.canAdd(x, y, s, orientation):
                  self.addShip(x, y, s, orientation)
                  done = True

  def hasLost(self):
    return all([self.ships[k].isSunk() for k in self.ships.keys()])
