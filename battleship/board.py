# Our Board class:
from pieces import *

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
