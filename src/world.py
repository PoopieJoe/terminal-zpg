import math
import json
import random
import numpy as np
import matplotlib.pyplot as plt
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
        self.cells = []
        self.cells = self.generateInitialNine()
        return

    def generateInitialNine(
        self
    )->list[cell.Cell]:

        cells = []
        sidelength = 3
        radius = math.floor(sidelength/2)
        for r in (0,-1,1):
            for c in (0,-1,1):
                newcell = self.generator.genCell(cells,c,r)
                cells.append(newcell)
                print("Cell: " + str((c,r)))
                # printmap(newcell.landmap,"Landmap Cell ({},{})".format(c,r))
            
        # plt.show()
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

def printmap(
    arr:np.ndarray,
    title=""
):
    # print('\n'.join('  '.join("{:} ".format(int(x)) for x in row) for row in arr.tolist()))
    plt.figure()
    plt.title(title)
    plt.imshow(arr.T,interpolation="none",origin='lower')
    return