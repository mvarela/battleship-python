from battleship.board import Board
from battleship.ai import AI
from battleship.player import Player
from enum import Enum
from random import choice

class Turn(Enum):
    player = 0
    ai = 1

class Game:
    def __init__(self, boardSize = 10, fleet = [2, 3, 3, 4, 5]):
        self.playerBoard = Board(boardSize, boardSize)
        print(boardSize)
        self.aiBoard = Board(boardSize, boardSize)
        self.aiBoard.populate(fleet)
        self.player = Player(self.playerBoard, self.aiBoard, fleet)
        self.nextTurn = choice(list(Turn))
        self.finished = False
        self.winner = None

    def playAI(self):
        if not(self.finished) and self.nextTurn == Turn.ai:
            self.ai.playTurn()
            self.nextTurn = Turn.player
            if self.playerBoard.hasLost():
                self.finished = True
                self.winner = Turn.ai

    def playPlayer(self, x, y):
        if not(self.finished) and self.nextTurn == Turn.player:
            self.player.fire(x, y)
            self.nextTurn = Turn.ai
            if self.aiBoard.hasLost():
                self.finished = True
                self.winner = Turn.player
