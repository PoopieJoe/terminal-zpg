import json
import random
from src.constants import *

class Cell:
    def __init__(self,type:str):
        self.type = type
        return

class Chunk:
    def __init__(
        self,
        id,
        data:list[list[Cell]] = None,
        neighbours:list[int] = None,
        width = CHUNKSIZEW,
        height = CHUNKSIZEH,
        offset = None,
        fill = Cell(WORLDTILETYPES.VOID)
    ):
        self.id = id
        self.isloaded = False
        self.data = data
        if self.data == None:
            self.data = [[fill for _ in range(width)] for _ in range(height)]
        if neighbours == None:
            self.neighbours = [None for _ in range(len(WINDDIRECTIONS.getlist()))]
        else:
            self.neighbours = neighbours    
        self.width = width
        self.height = height
        self.offset = offset
        return

    def getCell(
        self,
        x,y
    ) -> Cell:
        return self.data[x][y]

    def setCell(
        self,
        x,y,
        value:Cell
    ):
        self.data[x][y] = value
        return

    
class World:
    def __init__(
        self
    ):
        self.generator = WorldGenerator()
        print("Generating world...")
        self.chunks = self.generateInitial()
        return

    def generateInitial(
        self,
        chunkWidth = CHUNKSIZEW,
        chunkHeight = CHUNKSIZEH
    ):
        # generate base chunk
        origin = Chunk(0)

        # determine number of biome seeds
        nBiomes = random.randint(1,3)

        for _ in range(nBiomes):
            row = random.randint(0,chunkHeight-1)
            column = random.randint(0,chunkWidth-1)
            cell = origin.getCell(row,column)
            biome = random.choices(WORLDTILETYPES.getlist())
            cell.type = biome
            print("Seed placed at (" + str(row) + "," + str(column) + ")")

        chunks = [origin]
        for n in range(8):
            newchunk = Chunk(n+1)
            self.setNeighbours(origin,newchunk,WINDDIRECTIONS.getlist()[n])
            # Something something Perlin Noise for procedural generation
            chunks.append(newchunk)
            
        return chunks

    # TODO Away with the Neighbor system and just use coordinates, 
    # but do we keep the list (coord is a member of Chuck) 
    # or another 2D array of Chunks?

    def setNeighbours(
        self,
        srcChunk:Chunk,
        destChunk:Chunk,
        direction
    ):
        dir_n = WINDDIRECTIONS.getlist().index(direction)
        srcChunk.neighbours[dir_n] = destChunk.id
        oppositedir_n = dir_n-len(WINDDIRECTIONS.__dict__)
        destChunk.neighbours[oppositedir_n] = srcChunk.id

    def findOtherNeighbours(
        self,
        chunk:Chunk
    ):
        for dir,chunkid in enumerate(chunk.neighbours):
            if chunkid != 0:
                cui = self.chunks[chunkid]
                origindir = dir-len(WINDDIRECTIONS.getlist())
                if dir % 2 == 0: #cardinal directions
                    for offset in [-2,-1,1,2]:
                        if cui.neighbours[origindir+offset] != None:

        newNeighbours = list()
        return newNeighbours

    def getCell(
        self,
        x:int,
        y:int,
    ):
        return NotImplementedError

    def setCell(
        self,
        x:int,
        y:int,
        value:Cell
    ):
        return NotImplementedError

class WorldGenerator:
    def __init__(self):
        self.seed = random.randint(0,pow(2,64)-1) #initialize randomizer
        random.seed(self.seed)
        print("Generator initialized with seed: " + str(self.seed))

    def genChunk(
        self,
        neighbours
    ):
        return NotImplementedError

    def getCell(
        self,
        row:int,
        column:int,
    ):
        return NotImplementedError

    def setCell(
        self,
        row:int,
        column:int,
        value:Cell
    ):
        return NotImplementedError