import sys, os
from battleship.game import Game, Turn
from battleship.board import Orientation

class CLIDriver():
    def __init__(self):
        self.game = Game()
        self.playerBoard = self.game.playerBoard
        self.aiBoard = self.game.aiBoard
        self.renderBoards()
        self.playerInit()

    def renderBoards(self):
        os.system('clear')
        print('Your board\n')
        self.playerBoard.printBoard()
        print('Opponent\'s board \n')
        self.aiBoard.printBoard(opponentView=True)

    def doMenu(self, opts, prompt):
        self.renderBoards()
        print(prompt + ' (type "quit!" to quit)')
        for (i, text) in opts:
            print(str(i) + ' - ' + text)
        while True:
            choice = input("your choice: ")
            if(choice == "quit!"):
                exit(0)
            idx = [i for (i, t) in opts if str(i) == choice]
            if len(idx) > 0:
                return idx[0]

    def playerInit(self):
        print('Select your ship positions:')
        opts = [(1, "Automatic assignment"),
                (2, "Manual Assignment")]
        choice = self.doMenu(opts, "Automatic or manual?")
        if choice == 1:
            self.game.player.populateBoard()
        else:
            self.doManualPositioning()

    def doManualPositioning(self):
        player = self.game.player
        remainingShips = player.freeShips
        done = False
        while len(remainingShips) > 0 and not(done):
            opts = [(i, 'Length ' + str(remainingShips[i]))
                    for i in range(len(remainingShips))]
            lengthIdx = self.doMenu(opts, "Select ship length")
            length = remainingShips[lengthIdx]
            opts = [(o.value, o.name) for o in list(Orientation)]
            oIdx = self.doMenu(opts, "Select ship orientation")
            orientation = Orientation(oIdx)
            opts = [(i, str(i)) for i in range(0, self.playerBoard.width)]
            x = self.doMenu(opts, "Select ship column")
            y = self.doMenu(opts, "Select ship row")
            if(self.playerBoard.canAdd(x, y, length, orientation)):
                self.game.player.addShip(x, y, length, orientation)
            else:
                opts = [(1, "Continue Manually"), (2, "Place remaining ships automatically")]
                cont = self.doMenu(opts, "That position was not feasible, how do you want to continue?")
                if cont == 2:
                    self.game.player.populateBoard()
                    done = True

    def play(self):
        game = self.game
        while not game.finished:
            self.renderBoards()
            if game.nextTurn == Turn.ai:
                game.playAI()
            else:
                opts = [(i, str(i)) for i in range(0, self.aiBoard.width)]
                x = self.doMenu(opts, "Select target column")
                y = self.doMenu(opts, "Select target row")
                game.playPlayer(x, y)
        winner = game.winner.name
        print(winner + ' has won!')
        exit(0)
