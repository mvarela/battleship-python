# Our Board class:
from pieces import (EmptyPiece, WaterPiece,
                    ShipPiece, HitShipPiece)
from enum import Enum
from ship import Ship
from uuid import uuid4


class Orientation(Enum):
   horizontal = 0
   vertical = 1


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

  def rowString(self, n):
    if n <= self.height:
      rowStr = ' | '.join([self.grid[i][n].draw() for i in range(self.width)])
      return('| ' + rowStr + ' |\n')
    else:
      return ''

  def printBoard(self):
    rows = [self.rowString(i) for i in range(self.height)]
    for r in rows:
      print(r)

  def positions(self, x, y, length, orientation):
     """Auxiliary function to return the coordinates occupied by adding a ship"""
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

