import math
import json
import random
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
        data:list[list[Tile]] = None,
        neighbours:list[int] = None,
        width = CELLSIZEW,
        height = CELLSIZEH,
        fill = Tile(WORLDTILETYPES.VOID)
    ):
        self.isloaded = False
        self.data = data
        if self.data == None:
            self.data = [[fill for _ in range(width)] for _ in range(height)]
        if neighbours == None:
            self.neighbours = [None for _ in range(len(WINDDIRECTIONS.getlist()))]
        else:
            self.neighbours = neighbours    
        self.dimensions = (width,height)
        self.celloffset = (offsetx,offsety)
        self.tileoffset = (offsetx*width,offsety*height) + ORIGINOFFSET
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

    
class World:
    def __init__(
        self
    ):
        self.generator = WorldGenerator()
        print("Generating world...")
        self.cells = self.generateInitialNine()
        return

    def generateInitialNine(
        self,
        cellWidth = CELLSIZEW,
        cellHeight = CELLSIZEH
    )->list[Cell]:
        # generate base cell
        origin = Cell(0,0)

        # determine number of biome seeds
        nBiomes = random.randint(1,3)

        for _ in range(nBiomes):
            row = random.randint(0,cellHeight-1)
            column = random.randint(0,cellWidth-1)
            tile = origin.getTile((row,column))
            tile.type = random.choices(WORLDTILETYPES.getlist())
            print("Seed placed at (" + str(row) + "," + str(column) + ")")

        cells = []
        sidelength = 3
        radius = math.floor(sidelength/2)
        for r in range(-radius,radius+1):
            for c in range(-radius,radius+1):
                if r == 0 and c == 0:
                    cells.append(origin)
                else:
                    cells.append(Cell(r,c))
            
        return cells

    # Solution: keep list of cells with coord members, is robust for negative coordinates and dynamic cell generation

    def findCell(
        self,
        celloffset:tuple
    ):
        for cell in self.cells:
            if cell.celloffset == celloffset:
                return cell


    def coords2cellOffset(
        self,
        coords:tuple
    ):
        celloffsetx,tileoffsetx = divmod(coords[0],CELLSIZE[0])
        celloffsety,tileoffsety = divmod(coords[1],CELLSIZE[1])
        
        return (celloffsetx, celloffsety), (tileoffsetx,tileoffsety)

    def getTile(
        self,
        coord:tuple
    ):
        cellOffset,tileoffset = self.coords2cellOffset(coord)
        cell = self.findCell(cellOffset)
        return cell.getTile(tileoffset)

    def setTile(
        self,
        coord:tuple,
        value:Tile
    ):
        cellOffset,tileoffset = self.coords2cellOffset(coord)
        cell = self.findCell(cellOffset)
        return cell.setTile(tileoffset,value)

class WorldGenerator:
    def __init__(self):
        self.seed = random.randint(0,pow(2,64)-1) #initialize randomizer
        random.seed(self.seed)
        print("Generator initialized with seed: " + str(self.seed))

    def genCell(
        self
    ):
        return NotImplementedError

    def getTile(
        self,
        row:int,
        column:int,
    ):
        return NotImplementedError

    def setTile(
        self,
        row:int,
        column:int,
        value:Tile
    ):
        return NotImplementedError