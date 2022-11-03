import copy
from xmlrpc.client import Boolean

import numpy as np
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
        landmap:np.ndarray = None,
        heightmap:np.ndarray = None,
        biomemap:np.ndarray = None
    ):
        self.isloaded = False
        self.landmap = landmap
        self.heightmap = heightmap
        self.biomemap = biomemap

        self.celloffset = (offsetx,offsety)                             # offset in cells

        self.bottomleft = (offsetx*CELLSIZEW,offsety*CELLSIZEH)         # coordinate of the bottomleft tile
        self.topleft = (self.bottomleft[0],self.bottomleft[1]+CELLSIZEH-1)#etc
        self.topright = (self.bottomleft[0]+CELLSIZEW-1,self.bottomleft[1]+CELLSIZEH-1)
        self.bottomright = (self.bottomleft[0]+CELLSIZEW-1,self.bottomleft[1])
        return

    def getLand(
        self,
        coord:tuple
    ) -> int:
        return self.landmap[coord[0],coord[1]]

    def setTile(
        self,
        coord:tuple,
        value:Tile
    ) -> int:
        self.landmap[coord[0],coord[1]] = value
        return