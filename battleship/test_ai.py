from battleship.board import Board
from battleship.ai import AI
from hypothesis import given, strategies as st

@given(st.integers(min_value=5, max_value=50))
def testCheckerboard(side):
    b = Board(side, side)
    ai = AI(b)
    checkerboard = ai.checkerboardCoordinates()
    assert(len(checkerboard) == ((side * side) // 2))

@given(st.data())
def testGameCompletion(data):
    numberOfGames = data.draw(st.integers(min_value=1, max_value=50))
    for i in range(0, numberOfGames):
        b = Board(10, 10)
        b.populate([2, 3, 3, 4, 5])
        ai = AI(b)
        while not ai.finished:
            ai.playTurn()
        #assert(all([b.ships[k].isSunk() for k in b.ships.keys()]))
        assert(b.hasLost())
