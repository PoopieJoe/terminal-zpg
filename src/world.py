import math
import json
import random
import src.cell as cell
import src.worldgen as worldgen
from src.constants import *    
class World:
    def __init__(
        self
    ):
        seed = input("Give world seed: ")
        self.generator = worldgen.WorldGenerator(seed)
        print("Generating world...")
        self.cells = self.generateInitialNine()
        return

    def generateInitialNine(
        self
    )->list[cell.Cell]:

        print("Cell : " + str((0,0)))
        origin = self.generator.genCell(0,0)

        cells = []
        sidelength = 3
        radius = math.floor(sidelength/2)
        for r in range(-radius,radius+1):
            for c in range(-radius,radius+1):
                if r == 0 and c == 0:
                    cells.append(origin)
                else:
                    print("Cell: " + str((r,c)))
                    cells.append(self.generator.genCell(r,c))
            
        return cells

    # Solution: keep list of cells with coord members, is robust for negative coordinates and dynamic cell generation

    def findCell(
        self,
        celloffset:tuple
    ):
        for cell in self.cells:
            if cell.celloffset == celloffset:
                return cell
        return ValueError



    def coords2cellOffset(
        self,
        coords:tuple
    ):
        celloffsetx,tileoffsetx = divmod(coords[0],CELLSIZEW)
        celloffsety,tileoffsety = divmod(coords[1],CELLSIZEH)
        
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
        value:cell.Tile
    ):
        cellOffset,tileoffset = self.coords2cellOffset(coord)
        cell = self.findCell(cellOffset)
        return cell.setTile(tileoffset,value)
