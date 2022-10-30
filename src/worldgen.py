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
        self.rng = np.random.default_rng(int("".join([str(ord(char)) for char in seed])))

    def genCell(
        self,
        world,
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

        landmapshape = (CELLSIZEW//4,CELLSIZEH//4)

        # mask filter to blend raw generated map with surroundings
        blendfilter = np.empty(landmapshape)
        blendrange = 1/6
        for x in range(landmapshape[0]):
            for y in range(landmapshape[1]):
                d = max(abs(x-landmapshape[0]//2),abs(y-landmapshape[1]//2))
                blendfilter[x,y] = max(0,(d-1/blendrange)+1)
        blendfilter += noise.generatePerlinNoise2d(landmapshape,(4,4))*(blendfilter.max()/2)
        blendfilter *= 1/blendfilter.max()

        # Find neighbouring cells
        # East,West,North,South
        edges = {}
        fakeneighbour = self._genLandmap() # generate raw
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            try:
                neighbourland = self._findCell(world,(offsetx+dx,offsety+dy)).landmap
            except ValueError: # cell does not exist, use fake neighbor
                neighbourland = fakeneighbour

            # fetch opposite side
            match (dx,dy):
                case (1,0): #East
                    edges[WINDDIRECTIONS.EAST] = neighbourland[0,:] #fetch west column
                case (-1,0): #West
                    edges[WINDDIRECTIONS.WEST] = neighbourland[-1,:] #fetch east column
                case (0,1): #North
                    edges[WINDDIRECTIONS.NORTH] = neighbourland[:,0] #fetch south row
                case (0,-1): #South
                    edges[WINDDIRECTIONS.SOUTH] = neighbourland[:,-1] #fetch north row

        # create interpolated landmap
        # interpolate columns
        arrcolinterp = np.empty(landmapshape)
        for column in range(landmapshape[0]):
            newcoly = range(landmapshape[1])
            top = edges[WINDDIRECTIONS.NORTH][column]
            bottom = edges[WINDDIRECTIONS.SOUTH][column]
            colinterp = np.interp(newcoly,[-1,landmapshape[1]],[bottom,top])
            arrcolinterp[column,:] = colinterp

        arrrowinterp = np.empty(landmapshape)
        for row in range(landmapshape[1]):
            newrowx = range(landmapshape[0])
            right = edges[WINDDIRECTIONS.EAST][row]
            left = edges[WINDDIRECTIONS.WEST][row]
            rowinterp = np.interp(newrowx,[-1,landmapshape[0]],[left,right])
            arrrowinterp[:,row] = rowinterp

        interplandmap = ( arrcolinterp + arrrowinterp ) / 2
        
        # Land map
        # Scale = 1:2
        rawlandmap = self._genLandmap()

        # Total land map
        landmap = ( interplandmap*blendfilter + rawlandmap*(1-blendfilter) ) 

        # schmol gassian blur
        kernel =  1/16*np.array([   [1,2,1],
                                    [2,4,2],
                                    [1,2,1]])
        landmap = ndimage.convolve(landmap,kernel)
        

        # run cellular automata to smooth out

        # round to 1 or 0
        landmap = np.clip(np.rint(landmap),0,1)

        # Fill cell
        c = cell.Cell(offsetx,offsety,landmap) #cell.Cell(offsetx,offsety,rawlandmap.tolist())
        return c

    def _genLandmap(
        self
    ):

        def _addland(
            arr:np.ndarray,
            likelyhood
        ):
            w,h = arr.shape
            for c in range(w):
                for r in range(h):
                    if random.random() < likelyhood:
                        arr[c,r] = 1
            return arr

        # base array
        noise = 0.4
        w = CELLSIZEW//64
        h = CELLSIZEH//64
        landarr = np.zeros([w,h])

        # generate major landmass
        landarr = _addland(landarr,1/4)

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, clip=(0,1))

        # add minor landmasses
        landarr = _addland(landarr,1/3)

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, clip=(0,1))

        # add tiny islands
        landarr = _addland(landarr,1/16) # less common

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, iter=2, clip=(0,1))

        # pass with gassian noise to smooth out
        kernel =  1/16*np.array([   [1,2,1],
                                    [2,4,2],
                                    [1,2,1]])
        # kernel = 1/256*np.array([   [1,4,6,4,1],
        #                             [4,16,24,16,4],
        #                             [6,24,36,24,6],
        #                             [4,16,24,16,4],
        #                             [1,4,6,4,1]])
        landarr = ndimage.convolve(landarr,kernel)
        # landarr = np.rint(landarr)
        landarr = np.clip(landarr,0,1)

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
            arr = arr + 2*noisefactor*(self.rng.random(arr.shape)-0.5)
            arr = np.rint(arr) #round to integers

            # clip if limits are given
            if clip != None:
                arr = np.clip(arr,clip[0],clip[1])
            
        return arr

    def _findCell(
        self,
        cells:list[cell.Cell],
        celloffset:tuple
    ):
        for cell in cells:
            if cell.celloffset == celloffset:
                return cell
        raise ValueError


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
    plt.imshow(arr.T,interpolation="none",origin='lower')
    return