import math
import tkinter as tk
import src.control as control
import src.world as world
from src.constants import *

class MapRenderer(tk.Frame):
    def __init__(
        self,
        master,
        map:world.World,
        coords:tuple
    ):
        
        tk.Frame.__init__(self,master)

        # empty canvas
        tilesize = 10         # size of a tile in px
        renderareasize = 3    # render area size in chunks (3x3)
        mapCanvas = tk.Canvas(self,width=tilesize*renderareasize,height=tilesize*renderareasize,bg="white")

        # load relevant chunks (3x3 centered around character)
        radius = math.floor(renderareasize/2)
        charchunk,tileoffset = map.coords2cellOffset(coords)   # chunk of character

        renderarea = [[world.Tile(WORLDTILETYPES.VOID) for _ in range(renderareasize*CELLSIZEW)] for _ in range(renderareasize*CELLSIZEH)]

        topleftcoord = map.findCell((coords[0]-radius,coords[1]+radius)).topleft #this coordinate is mapped to 0,0 on the canvas

        for celloffsetx in range(charchunk[0]-radius,charchunk[0]+radius):
            for celloffsety in range(charchunk[1]-radius,charchunk[1]+radius):
                cell = map.findCell((celloffsetx,celloffsety))

                for xoffset in range(CELLSIZEW):
                    for yoffset in range(CELLSIZEH):
                        tile = cell.getTile((xoffset,yoffset))
                        
                        rendercellcoord = (cell.topleft[0]-topleftcoord[0]+xoffset,cell.topleft[1]-topleftcoord[1]+yoffset)
                        renderarea[rendercellcoord[0]][rendercellcoord[1]] = tile
        print(renderarea)


        
        


        

