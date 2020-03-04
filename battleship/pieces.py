class Piece():
    def draw(this, opponentView = False):
        return " "

    def isEmpty(this):
      return True

class EmptyPiece(Piece):
    pass

class WaterPiece(Piece):
    def draw(this, opponentView = False):
        return "W"

class ShipPiece(Piece):
    def __init__(this, shipId, index):
        """

        """
        this.shipId = shipId
        this.index = index
    def draw(this, opponentView = False):
        if opponentView:
            return " "
        else:
            return "S"

    def isEmpty(this):
      return False


class HitShipPiece(ShipPiece):
    def draw(this, opponentView = False):
        return "H"

    def isEmpty(this):
      return False
