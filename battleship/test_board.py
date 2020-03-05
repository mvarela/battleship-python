from battleship.board import Board, Orientation
from battleship.ship import Ship
from battleship.pieces import EmptyPiece, WaterPiece, ShipPiece, HitShipPiece
from hypothesis import given, strategies as st


@given(st.integers(min_value=0, max_value=9),
       st.integers(min_value=0, max_value=9),
       st.integers(min_value=2, max_value=5),
       st.sampled_from(Orientation))
def testShipAdd(x, y, length, orientation):
    """We test that we can add valid combinations of coordinates, lengths and orientations to a board"""
    b = Board(10,10)
    if orientation == Orientation.vertical:
        if(y + length < b.height):
            assert(True == b.addShip(x, y, length, orientation))
        else:
          assert(False == b.addShip(x, y, length, orientation))
    else:
        if(x + length < b.width):
            assert(True == b.addShip(x, y, length, orientation))
        else:
          assert(False == b.addShip(x, y, length, orientation))


def auxCoordsSameAxis(x, y, length, orientation):
    """Auxiliary function for the test below"""
    if orientation == Orientation.horizontal:
        xrange =  [i for i in
                   range(x - (length // 2), x + (length // 2))
                   if i >= 0]
        yrange = [y]
    else:
        xrange = [x]
        yrange = [i for i in
                  range(y - (length // 2), y + (length //2))
                  if i >= 0]
    return [(i, j) for i in xrange for j in yrange]

def auxCoordsOppositeAxis(x, y, length):
    """Auxiliary function for the test below"""
    xrange =  [i for i in
               range(x - (length // 2), x + (length // 2))
               if i >= 0]
    yrange = [i for i in
              range(y - (length // 2), y + (length //2))
              if i >= 0]
    return [(i, j) for i in xrange for j in yrange]

@given(st.data())
def testNonOverlappingShips(data):
    """We test that given a randomly placed (random) ship, another similar ship
cannot be placed in an overlapping position. We check for overlapping positions in
    the both orientations"""

    opposites = {Orientation.horizontal : Orientation.vertical,
                 Orientation.vertical : Orientation.horizontal}
    side = 10
    lengthGen = st.integers(min_value=2, max_value=5)
    length = data.draw(lengthGen)
    orientation = data.draw(st.sampled_from(Orientation))
    startingCoord = st.integers(min_value = 0, max_value = (side - length))
    x = data.draw(startingCoord)
    y = data.draw(startingCoord)
    b = Board(side, side)
    if(b.canAdd(x, y, length, orientation)):
        b.addShip(x, y, length, orientation)
        sameOrientationCoords = auxCoordsSameAxis(x, y, length, orientation)
        sameOrientationChecks = [b.canAdd(i, j, length, orientation)
                                 for (i, j) in sameOrientationCoords]
        assert(not(any(sameOrientationChecks)))
        newOrientation = opposites[orientation]
        newOrientationCoords = auxCoordsOppositeAxis(x, y, length)
        newOrientationChecks = [b.canAdd(i, j, length, newOrientation)
                                for (i, j) in newOrientationCoords]
        print(not(any(newOrientationChecks)))



@given(st.data())
def testShipFire(data):
    """We check that given a list of firing coordinates on the board, after firing, the
    number of `HitShipPiece` instances on the grid is the same as the sum of cardinalities
    for all the ships' hits on the board (populated as per the game rules)."""
    b = Board(10,10)
    b.populate([2, 3, 3, 4, 5])
    coords = st.tuples(st.integers(min_value=0, max_value=9),
                       st.integers(min_value=0, max_value=9))
    fireCoordinates = data.draw(st.lists(coords, min_size = 1, max_size = 50))
    for (x, y) in fireCoordinates:
        b.fire(x, y)
    hitPieces = sum([1 for i in range(0, b.width) for j in range(0, b.height)
                     if isinstance(b.grid[i][j], HitShipPiece)])
    cardinalities = sum([len(b.ships[k].hits) for k in b.ships.keys()])
    assert(hitPieces == cardinalities)
