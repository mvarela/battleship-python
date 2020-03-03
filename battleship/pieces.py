class Piece():
    def draw(this):
        return " "

    def isEmpty(this):
      return true

class EmptyPiece(Piece):
    def draw(this):
        return "E"

class WaterPiece(Piece):
    def draw(this):
        return "W"

class ShipPiece(Piece):
    def __init__(this, shipId, index):
        """

        """
        this.shipId = shipId
        this.index = index
    def draw(this):
        return "S"

    def isEmpty(this):
      return false


class HitShipPiece(ShipPiece):
    def draw(this):
        return "H"

    def isEmpty(this):
      return false
