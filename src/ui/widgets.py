import math
import tkinter as tk
import src.control as control
import src.world as world
from src.constants import *

class MapRenderer(tk.Frame):
    def __init__(
        self,
        master,
        world:world.World,
        coords:tuple
    ):
        from world import World,Cell,Tile
        tk.Frame(master)

        renderareasize = 3    # render area size in chunks (3x3)

        # load relevant chunks (3x3 centered around character)
        radius = math.floor(renderareasize/2)
        charchunk,tileoffset = world.coords2cellOffset(coords)   # chunk of character
        renderedchunks = []
        for xoffset in range(charchunk[0]-radius,charchunk[0]+radius+1):
            rowarr = []
            for yoffset in range(charchunk[1]-radius,charchunk[1]+radius+1):
                rowarr.append(world.findCell((xoffset,yoffset)))
            renderedchunks.append(rowarr)


        renderarea = []
        for xoffset in range(renderareasize*CELLSIZEW):
            rowarr = []
            for yoffset in range(renderareasize*CELLSIZEH):
                rowarr.append(Tile(WORLDTILETYPES.VOID))
            renderarea.append(rowarr)

        
        

        # empty canvas
        tilesize = 10                   # size of a tile in px
        mapCanvas = tk.Canvas(self,width=tilesize*renderareasize,height=tilesize*renderareasize,bg="white")

