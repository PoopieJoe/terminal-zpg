import copy
from src.constants import *


class Tile:
    def __init__(self,type:str):
        self.type = type
        return

class Cell:
    def __init__(
        self,
        offsetx:int,
        offsety:int,
        landmap = None
    ):
        self.isloaded = False
        # if fill == None:
        #     self.data = [[Tile(WORLDTILETYPES.VOID) for _ in range(CELLSIZEW)] for _ in range(CELLSIZEH)]
        # else:
        #     self.data = [[Tile(fill) for _ in range(CELLSIZEW)] for _ in range(CELLSIZEH)]
        self.landmap = landmap

        self.celloffset = (offsetx,offsety)                             # offset in cells

        self.bottomleft = (offsetx*CELLSIZEW,offsety*CELLSIZEH)         # coordinate of the bottomleft tile
        self.topleft = (self.bottomleft[0],self.bottomleft[1]+CELLSIZEH-1)#etc
        self.topright = (self.bottomleft[0]+CELLSIZEW-1,self.bottomleft[1]+CELLSIZEH-1)
        self.bottomright = (self.bottomleft[0]+CELLSIZEW-1,self.bottomleft[1])
        return

    def getTile(
        self,
        coord:tuple
    ) -> Tile:
        return self.data[coord[0]][coord[1]]

    def setTile(
        self,
        coord:tuple,
        value:Tile
    ):
        self.data[coord[0]][coord[1]] = value
        return