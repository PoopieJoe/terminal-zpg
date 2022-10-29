import random
from collections import Counter
import time
import src.cell as cell
from src.constants import *

class WorldGenerator:
    def __init__(self,seed):
        random.seed(seed)

    def genCell(
        self,
        offsetx,
        offsety
    ):
        # For future overhaul
        # Inspiration: https://www.alanzucconi.com/2022/06/05/minecraft-world-generation/
        # Interesting resources: Fractal noise, Fractal Brownian motion noise, Perlin Noise, Simplex Noise
        # Basic idea:
        # First binary map (sea vs land) (scale 1x1:64x64)
        # Cellular automata to refine map
        # Zoom to create details
        # Create climate detail maps (temperature map, humidity map, etc.)
        # Create height map to determine rivers
        
        #hollow cell
        c = cell.Cell(offsetx,offsety,WORLDTILETYPES.OCEAN)

        # determine number of biome seeds
        nBiomeSeeds = random.randint(8,16)
        
        for i in range(nBiomeSeeds): # repeat for every seed
            if ((offsetx,offsety) == (0,0) # first biome in the origin cell is always plains placed at the origin
                and i == 0):
                row,column = (CELLSIZEW//2,CELLSIZEH//2)
                seed = c.getTile((column,row))
                seed.type = WORLDTILETYPES.PLAINS 
            else:
                row = random.randint(0,CELLSIZEH-1)
                column = random.randint(0,CELLSIZEW-1)
                seed = c.getTile((column,row))
                seed.type = random.choices(WORLDGENERATORTILES)[0]
            # print("Seed placed at (" + str(row) + "," + str(column) + ") of type: " + seed.type)

            # let the seed spread into a blob
            minspread,maxspread = BIOMESPREADMAP[seed.type]
            spreadchance = minspread + (maxspread-minspread)*random.random() #random value between minspread and 1
            decayrate = 0.01    # rate at which spread chance decays
            diagonalmodifier = 2 ** -0.5    #diagonals are scaled to distance, makes blobs less square
            spreadrange = 1 #numbers > 1 make it slower and the biomes more
            blob = [{
                "coord":(column,row),
                "tile":seed
            }]

            while spreadchance > 0:     # run until spread chance is too low
                newblob = []
                for tile in blob:       # run for newly generated layer
                    for tileoffsetx in range(-spreadrange,spreadrange+1):
                        for tileoffsety in range(-spreadrange,spreadrange+1):
                            coord = (tile["coord"][0]+tileoffsetx,tile["coord"][1]+tileoffsety)# check surrounding tiles
                            if( (tileoffsetx,tileoffsety) != (0,0)
                                and coord[0] < CELLSIZEW
                                and coord[1] < CELLSIZEH):
                                sel_tile = c.getTile(coord)
                                if (tileoffsetx,tileoffsety) in ((1,1),(1,-1),(-1,1),(-1,-1)): # scale diagonal spread chance down
                                    spreadmod = diagonalmodifier
                                else:
                                    spreadmod = 1
                                if( random.random() < spreadchance*spreadmod
                                    and sel_tile.type != seed.type):
                                    sel_tile.type = seed.type
                                    newblob.append({
                                        "coord":coord,
                                        "tile":sel_tile
                                    })
                blob = newblob
                spreadchance = spreadchance - decayrate

        # run cellular automata logic
        CAiterations = 3
        for _ in range(CAiterations):
            newdata = [[None for _ in range(CELLSIZEW)] for _ in range(CELLSIZEH)]
            
            for row in range(CELLSIZEH):
                for col in range(CELLSIZEH):
                    tile = c.getTile((col,row))
                    sur_tiles = [] #surrounding tiles
                    for tileoffsetx,tileoffsety in ((-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,-1),(-1,1),(1,-1)):
                        coord = (col+tileoffsetx,row+tileoffsety)# fetch surrounding tiles
                        if( coord[0] < CELLSIZEW
                            and coord[1] < CELLSIZEH):
                            sur_tiles.append(c.getTile(coord).type)

                    #smooth out edges
                    counts = Counter(sur_tiles)
                    newtype = counts.most_common(1)[0][0] # set to its majority
                    if newtype != tile.type:
                        newdata[col][row] = cell.Tile(newtype) #orphans are assimilated
                    else:
                        newdata[col][row] = tile
            c.data = newdata
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

# spreadchance per biome (minspreadchance,maxspreadchance)
BIOMESPREADMAP = {
    WORLDTILETYPES.DESERT:      (0.55,0.65),
    WORLDTILETYPES.FOREST:      (0.6,0.75),
    WORLDTILETYPES.OCEAN:       (0.4,0.6),
    WORLDTILETYPES.PLAINS:      (0.6,0.75),
    WORLDTILETYPES.TUNDRA:      (0.4,0.5),
    WORLDTILETYPES.MOUNTAIN:    (0.3,0.6),
}