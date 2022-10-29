from time import time, time_ns
import time
from collections import Counter
import src.worldgen as worldgen
from src.constants import *

generator = worldgen.WorldGenerator(time.time_ns()) # just random seed every time
nCells = 100

cellReport = []
for i in range(nCells):
    print("Cell " + str(i+1) + " out of " + str(nCells))
    newcell = generator.genCell(0,0)
    # count number of tiles of each biome
    types = []
    for col in newcell.data:
        for tile in col:
            types.append(tile.type)
    counts = Counter(types)
    cellReport.append(counts)

# summarize counts
summary = sum(cellReport,Counter())
totaltiles = CELLSIZEH*CELLSIZEW*nCells
for key in summary:
    val = summary[key]/totaltiles*100
    print("{:16}: {:.2f}%".format(key,val))