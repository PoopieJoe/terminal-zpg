import random
import src.cell as cell
from src.constants import *

class WorldGenerator:
    def __init__(self):
        self.seed = random.randint(0,pow(2,64)-1) #initialize randomizer
        random.seed(self.seed)
        print("Generator initialized with seed: " + str(self.seed))

    def genCell(
        self,
        offsetx,
        offsety
    ):
        #hollow cell
        c = cell.Cell(offsetx,offsety)

        # determine number of biome seeds
        nBiomeSeeds = random.randint(10,20)
        
        for _ in range(nBiomeSeeds):
            row = random.randint(0,CELLSIZEH-1)
            column = random.randint(0,CELLSIZEW-1)
            seed = c.getTile((row,column))
            seed.type = random.choices(WORLDGENERATORTILES)[0]
            # print("Seed placed at (" + str(row) + "," + str(column) + ") of type: " + seed.type)

            # let the seed spread into a blob
            spreadchance = 1
            decayrate = 0.1
            blob = [{
                "coord":(row,column),
                "tile":seed
            }]

            # find surrounding tiles
            while spreadchance > 0:
                newblob = []
                for tile in blob:
                    for tileoffsetx in range(-2,1+1):
                        for tileoffsety in range(-2,2+1):
                            coord = (tile["coord"][0]+tileoffsetx,tile["coord"][1]+tileoffsety)
                            if( (tileoffsetx,tileoffsety) != (0,0)
                                and coord[0] < CELLSIZEW
                                and coord[1] < CELLSIZEH):
                                sel_tile = c.getTile(coord)
                                if( random.random() < spreadchance
                                    and sel_tile.type != seed.type):
                                    sel_tile.type = seed.type
                                    newblob.append({
                                        "coord":coord,
                                        "tile":sel_tile
                                    })
                blob = newblob
                spreadchance = spreadchance - decayrate
            #repeat


        return c

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
        value:cell.Tile
    ):
        return NotImplementedError