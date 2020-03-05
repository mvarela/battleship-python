from hypothesis import given, strategies as st
from battleship.game import Game, Turn
from random import choice

@given(st.data())
def testFullGame(data):
    """We play a number of games, AI vs dummy player, and verify that each game
    has a single winning board"""
    numberOfGames = data.draw(st.integers(min_value = 10,
                                          max_value = 30))
    for i in range(1, numberOfGames):
        game = Game()
        side = game.playerBoard.width
        coords = [(i, j) for i in range(0, side) for j in range(0, side)]
        while not game.finished:
            if game.nextTurn == Turn.ai:
                game.playAI()
            else:
                elem = (x, y) = choice(coords)
                coords.remove(elem)
                game.playPlayer(x, y)
        assert((game.aiBoard.hasLost() and not(game.playerBoard.hasLost()) or
                (not(game.aiBoard.hasLost()) and game.playerBoard.hasLost())))
