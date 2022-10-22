import json
import random
from src.constants import *

class Cell:
    def __init__(self,type=str):
        self.type = type
        return
class World:
    def __init__(
        self
    ):
        self.generator = WorldGenerator()

        print("Generating world...")
        self.map = self.generator.generate()
        return

    def getCell(
        self,
        row:int,
        column:int,
    ):
        return self.map[row][column]

    def setCell(
        self,
        row:int,
        column:int,
        value:Cell
    ):
        self.map[row][column] = value

class WorldGenerator:
    def __init__(self):
        self.seed = random.randint(0,pow(2,64)-1) #initialize randomizer
        random.seed(self.seed)
        print("Generator initialized with seed: " + str(self.seed))

    def generate(
        self,
        width = 10,
        height = 10
    ):
        # generate empty ocean map
        self.map = [[Cell(WORLDTILETYPES.OCEAN) for _ in range(width)] for _ in range(height)]

        # determine number of biome seeds
        nBiomes = random.randint(2,4)

        for n in range(0,nBiomes):
            row = random.randint(0,self.height-1)
            column = random.randint(0,self.height-1)
            cell = self.getCell(row,column)
            biome = random.choices(list(WORLDTILETYPES.__dict__.values()))
            cell.type = biome
            print("Seed placed at (" + str(row) + "," + str(column) + ")")

        # Something something Perlin Noise for procedural generation

    def getCell(
        self,
        row:int,
        column:int,
    ):
        return self.map[row][column]

    def setCell(
        self,
        row:int,
        column:int,
        value:Cell
    ):
        self.map[row][column] = value