import random
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import src.noise as noise
import src.cell as cell
from src.constants import *

class WorldGenerator:
    def __init__(self,seed):
        random.seed(seed)
        self.rng = np.random.default_rng(sum([ord(char) for char in seed]))

    def genCell(
        self,
        offsetx,
        offsety
    ):
        # For future overhaul
        # Inspiration: https://www.alanzucconi.com/2022/06/05/minecraft-world-generation/
        # Interesting resources: 
        # Noise: Fractal noise, Fractal Brownian motion noise, Perlin Noise, Simplex Noise
        # Terrain generation: Voronoi diagrams, Diamond Square
        # Basic idea:
        # First binary map (sea vs land) (scale 1x1:64x64)
        # Cellular automata to refine map
        # Zoom to create details
        # Create climate detail maps (temperature map, humidity map, etc.)
        # Create biome borders
        # Map biomes to climate maps
        # Create height map to determine rivers
        
        # Land map
        # Scale = 1:32
        # Land:Ocean odds = 25/100
        landmap = self._genLandmap()
        printmap(landmap,"Land map 1:2")

        randnoise = noise.generateFractalNoise2d(landmap.shape,(8,8))
        printmap(randnoise,"noise")

        plt.show()
        return cell

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

    def _genLandmap(
        self
    ):
        # base array
        noise = 0.4
        w = CELLSIZEW//32
        h = CELLSIZEH//32
        landarr = np.zeros([w,h])

        # generate major landmass
        self._addland(landarr,1/4)

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, clip=(0,1))

        # add minor landmasses
        self._addland(landarr,1/4)

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, clip=(0,1))

        # add tiny islands
        self._addland(landarr,1/8) # less common

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, iter=2, clip=(0,1))
        return landarr

    def _upscale2dwithnoise(
        self,
        arr:np.ndarray,
        n = 2,
        noisefactor = 0,
        iter = 1,
        clip = None
    ) -> np.ndarray:
        # upscale layer by factor n
        for _ in range(iter):
            # cubic interpolation
            arr = ndimage.zoom(arr,zoom=n)

            # add linear noise between -rfactor and +rfactor
            arr = np.rint(arr + 2*noisefactor*(self.rng.random(arr.shape)-0.5)) 
            arr = np.rint(arr) #round to integers

            # clip if limits are given
            if clip != None:
                arr = np.clip(arr,clip[0],clip[1])
            
        return arr

    def _addland(
        self,
        arr:np.ndarray,
        likelyhood
    ):
        w,h = arr.shape
        for c in range(w):
            for r in range(h):
                if random.random() < likelyhood:
                    arr[c][r] = 1
        return arr


# spreadchance per biome (minspreadchance,maxspreadchance)
BIOMESPREADMAP = {
    WORLDTILETYPES.DESERT:      (0.55,0.65),
    WORLDTILETYPES.FOREST:      (0.6,0.75),
    WORLDTILETYPES.OCEAN:       (0.4,0.6),
    WORLDTILETYPES.PLAINS:      (0.6,0.75),
    WORLDTILETYPES.TUNDRA:      (0.4,0.5),
    WORLDTILETYPES.MOUNTAIN:    (0.3,0.6),
}

def printmap(
    arr:np.ndarray,
    title=""
):
    # print('\n'.join('  '.join("{:} ".format(int(x)) for x in row) for row in arr.tolist()))
    plt.figure()
    plt.title(title)
    plt.imshow(arr,interpolation="none")
    return