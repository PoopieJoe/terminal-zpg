class Tile:
    def __init__(self,type:str):
        self.type = type
        return

from src.constants import *

class Cell:
    def __init__(
        self,
        offsetx:int,
        offsety:int,
        data:list[list[Tile]] = None,
        neighbours:list[int] = None
    ):
        self.isloaded = False
        self.data = data
        if self.data == None:
            self.data = [[Tile(WORLDTILETYPES.VOID) for _ in range(CELLSIZEW)] for _ in range(CELLSIZEH)]
        if neighbours == None:
            self.neighbours = [None for _ in range(len(WINDDIRECTIONS.getlist()))]
        else:
            self.neighbours = neighbours    
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