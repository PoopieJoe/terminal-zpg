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

    def genMap(
        self
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
        # Scale = 1:4
        landmap = self._genLandmap(w=WORLDSIZEW//512,h=WORLDSIZEH//512)

        print("Generated landmap")

        # heightmap
        rawheightmap = noise.generateFractalNoise2d(    (landmap.shape[0],landmap.shape[1]),
                                                        (landmap.shape[0]//128,landmap.shape[1]//128),
                                                        generator=self.rng,
                                                        octaves=4,
                                                        persistence=0.4)
        rawheightmap -= rawheightmap.min()
        rawheightmap /= rawheightmap.max()

        print("Generated raw heightmap")
        
        # Land blendmap
        nlayers = 9 #multiple of 2+1
        offlayers = nlayers-1
        layers = []
        erosionlayer = landmap
        dilationlayer = landmap
        for i in range(offlayers//2):
            layers.append(erosionlayer)
            layers.append(dilationlayer)
            erosionlayer = ndimage.binary_erosion(erosionlayer)
            dilationlayer = ndimage.binary_dilation(dilationlayer)
        blendmap = sum(layers)/offlayers

        # heightoffset = 0.5#(heightmap.max() - heightmap.min())/2
        heightmap = offlayers*(rawheightmap+blendmap)/2-offlayers/2
        print("Blended heightmap with landmap")
        # layerdheightmap = np.rint(heightmap)
        print("Generated height layers")
        
        # place rivers
        rivers,nrivers,nlakes = self._placerivers(heightmap)
        print("Generated " + str(nrivers) + " rivers and " +str(nlakes) + " lakes")

        # generate biomes
        tempmap = noise.generateFractalNoise2d(         (landmap.shape[0],landmap.shape[1]),
                                                        (landmap.shape[0]//256,landmap.shape[1]//256),
                                                        generator=self.rng,
                                                        octaves=2)
        tempmap -= tempmap.min()
        tempmap /= tempmap.max()
        #discretize into 3 categories
        tempmap = np.rint(2*tempmap) #0,1,2

        rainmap = noise.generateFractalNoise2d( (landmap.shape[0],landmap.shape[1]),
                                                (landmap.shape[0]//256,landmap.shape[1]//256),
                                                generator=self.rng,
                                                octaves=2)
        rainmap -= rainmap.min()
        rainmap /= rainmap.max()
        rainmap = np.rint(2*rainmap) #0,1,2

        #divvy biomes
        strlen = 16
        biomemap = np.chararray((heightmap.shape[0],heightmap.shape[1],strlen))
        for c in range(biomemap.shape[0]):
            for r in range(biomemap.shape[1]):
                temp = tempmap[c,r]
                rain = rainmap[c,r]
                if temp == 0:
                    if rain == 0:
                        biomemap[c,r] = WORLDTILETYPES.TUNDRA
                    elif rain == 1:
                        biomemap[c,r] = WORLDTILETYPES.TAIGA
                    else:
                        biomemap[c,r] = WORLDTILETYPES.TAIGA
                elif temp == 1:
                    if rain == 0:
                        biomemap[c,r] = WORLDTILETYPES.PLAINS
                    elif rain == 1:
                        biomemap[c,r] = WORLDTILETYPES.FOREST
                    else:
                        biomemap[c,r] = WORLDTILETYPES.FOREST
                else:
                    if rain == 0:
                        biomemap[c,r] = WORLDTILETYPES.DESERT
                    elif rain == 1:
                        biomemap[c,r] = WORLDTILETYPES.PLAINS
                    else:
                        biomemap[c,r] = WORLDTILETYPES.JUNGLE
        print("Generated biomes")

        print("Upscaling...")
        # zoom in to full scale
        landmap = self._upscale2dwithnoise(landmap,n=2,noisefactor=0.4,iter=3,clip=(0,1))
        heightmap = self._upscale2dwithnoise(heightmap,n=2,iter=3)
        biomemap = self._upscale2dother(biomemap,n=2**3)
        plt.show()

        # split into smaller cells
        ncellsw = WORLDSIZEW//CELLSIZEW
        ncellsh = WORLDSIZEH//CELLSIZEH
        centercellx = ncellsw//2
        centercelly = ncellsh//2

        cells = []
        for cellcol in range(ncellsw):
            for cellrow in range(ncellsh):
                toplefttilex = cellcol*CELLSIZEW
                toplefttiley = cellrow*CELLSIZEH
                celloffsetx = cellcol - centercellx
                celloffsety = cellrow - centercelly
                newcell = cell.Cell(celloffsetx,celloffsety,
                                                landmap[toplefttilex:toplefttilex+CELLSIZEW-1,toplefttiley:toplefttiley+CELLSIZEH-1],
                                                heightmap[toplefttilex:toplefttilex+CELLSIZEW-1,toplefttiley:toplefttiley+CELLSIZEH-1],
                                                biomemap[toplefttilex:toplefttilex+CELLSIZEW-1,toplefttiley:toplefttiley+CELLSIZEH-1])
                cells.append(newcell)
        print("Done")
        return cells

    def _genLandmap(
        self,
        w = WORLDSIZEW//512,
        h = WORLDSIZEH//512
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
        landarr = np.zeros([w,h])

        # generate major landmass
        landarr = _addland(landarr,1/4)

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, clip=(0,1))

        # add minor landmasses
        landarr = _addland(landarr,1/4)

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, iter=2, clip=(0,1))

        # add islands
        landarr = _addland(landarr,1/16) # less common

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, iter=2, clip=(0,1))

        # add small islands
        landarr = _addland(landarr,1/256) # less common

        # upscale by 2 and slightly randomize values
        landarr = self._upscale2dwithnoise(landarr, n=2, noisefactor = noise, iter=1, clip=(0,1))

        # pass with gassian noise to smooth out
        # kernel =  1/16*np.array([   [1,2,1],
        #                             [2,4,2],
        #                             [1,2,1]])
        kernel = gaussKern(2,1.)
        landarr = ndimage.convolve(landarr,kernel)
        landarr = np.clip(np.rint(landarr),0,1)
        
        # run cellular automata to smooth out

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

            # add linear noise between -noisefactor and +noisefactor
            arr = arr + 2*noisefactor*(self.rng.random(arr.shape)-0.5)
            
            # clip if limits are given
            if clip != None:
                arr = np.rint(arr) #round to integers
                arr = np.clip(arr,clip[0],clip[1])
            
        return arr

    def _upscale2dother(
        self,
        arr:np.ndarray,
        n=2
    ):
        newarr = np.repeat(arr,n,axis=0)
        newarr = np.repeat(newarr,n,axis=1)
        return newarr

    def _placerivers(
        self,
        heightmap:np.ndarray
    ):
        def randomizeDirection(direction:tuple,changechance):
            if direction == (0,0): return (0,0) # no change
                
            directions = ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1))
            dirindex = directions.index(direction)
            roll = random.random()
            if roll<changechance/2:
                return directions[(dirindex+1)%len(directions)]
            elif roll<changechance:
                return directions[(dirindex-1)%len(directions)]
            else:
                return direction

        tmpheightmap = heightmap#pooling(heightmap,(2,2),'mean') # zoom out to make it faster
        rivermap = np.zeros(tmpheightmap.shape)

        # start rivers
        w,h = tmpheightmap.shape
        relheightmap = tmpheightmap/tmpheightmap.max()
        likelyhood = 0.01*relheightmap
        gradius = 3
        maxlakesize = 3
        nrivers = 0
        nlakes = 0
        for c in range(w):
            for r in range(h):
                if(random.random() < likelyhood[c,r]):
                    # weighted drunk walk
                    riverlen = 0
                    lastdirection = (0,0)
                    while(  tmpheightmap[c,r] > -1
                            and riverlen < 1000
                            and (c >= gradius and c <= w-gradius and r >= gradius and r <= h-gradius)):
                        # fetch local gradient
                        gradient = tmpheightmap[c-gradius:c+gradius+1,r-gradius:r+gradius+1]-tmpheightmap[c,r]
                        #pick highest downward gradient
                        desireddirection = np.unravel_index(gradient.argmin(),gradient.shape)
                        desireddirection = (math.ceil(desireddirection[0]/gradius) - 1,math.ceil(desireddirection[1]/gradius) - 1)
                        if desireddirection == (0,0): # found a minimum
                            # create lake
                            lakesize = max(int(maxlakesize*random.random()),1)
                            rivermap[c-lakesize:c+lakesize+1,r-lakesize:r+lakesize+1] = 1
                            nlakes += 1
                        #now randomize
                        if random.random()<0.5: # see if we go toward the lower gradient
                            direction = desireddirection
                        else:
                            direction = lastdirection
                        direction = randomizeDirection(direction,0.5) #local meandering

                        # step in that direction
                        c += direction[0]
                        r += direction[1]

                        if rivermap[c,r]: break # met another river
                        rivermap[c,r] = 1
                        riverlen +=1
                        lastdirection = direction

                    if riverlen > 0:
                        nrivers += 1
        
        rivermap = ndimage.binary_dilation(rivermap,iterations=2)
        # kernel = gaussKern(l=2,sig=1)
        # rivermap = ndimage.convolve(rivermap,kernel)        
        # rivermap = np.clip(np.rint(rivermap),0,1)
        return rivermap,nrivers,nlakes

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

def gaussKern(l=5, sig=1.):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)

def pooling(mat,ksize,method='max',pad=False):
    '''Non-overlapping pooling on 2D or 3D data.

    <mat>: ndarray, input array to pool.
    <ksize>: tuple of 2, kernel size in (ky, kx).
    <method>: str, 'max for max-pooling, 
                   'mean' for mean-pooling.
    <pad>: bool, pad <mat> or not. If no pad, output has size
           n//f, n being <mat> size, f being kernel size.
           if pad, output has size ceil(n/f).

    Return <result>: pooled matrix.
    '''

    m, n = mat.shape[:2]
    ky,kx=ksize

    _ceil=lambda x,y: int(np.ceil(x/float(y)))

    if pad:
        ny=_ceil(m,ky)
        nx=_ceil(n,kx)
        size=(ny*ky, nx*kx)+mat.shape[2:]
        mat_pad=np.full(size,np.nan)
        mat_pad[:m,:n,...]=mat
    else:
        ny=m//ky
        nx=n//kx
        mat_pad=mat[:ny*ky, :nx*kx, ...]

    new_shape=(ny,ky,nx,kx)+mat.shape[2:]

    if method=='max':
        result=np.nanmax(mat_pad.reshape(new_shape),axis=(1,3))
    else:
        result=np.nanmean(mat_pad.reshape(new_shape),axis=(1,3))

    return result