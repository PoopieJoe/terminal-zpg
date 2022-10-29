import math
import tkinter as tk
from tkinter.tix import CELL
import src.control as control
import src.cell as cell
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
        framew = SCREENW
        frameh = SCREENH    
        framesize = min(frameh,framew) # take minimum to be square

        # empty canvas
        renderareasize = 3      # render area size in chunks (3x3)
        tilesize = (math.floor(framesize/(renderareasize*CELLSIZEW)),math.floor(framesize/(renderareasize*CELLSIZEW)))            # size of a tile in px
        width, height = tuple([renderareasize*CELLSIZE[0]*tilesize[0],renderareasize*CELLSIZE[1]*tilesize[1]])
        mapCanvas = tk.Canvas(self,width=width,height=height,bg="white")
        mapCanvas.pack()

        # load relevant chunks (3x3 centered around character)
        radius = math.floor(renderareasize/2)
        charchunk,tileoffset = map.coords2cellOffset(coords)   # chunk of character

        topleftcoord = map.findCell((coords[0]-radius,coords[1]+radius)).topleft #this coordinate is mapped to 0,0 on the canvas

        for celloffsetx in range(charchunk[0]-radius,charchunk[0]+radius+1):
            for celloffsety in range(charchunk[1]-radius,charchunk[1]+radius+1):
                currentCell = map.findCell((celloffsetx,celloffsety))

                for xoffset in range(CELLSIZEW):
                    for yoffset in range(CELLSIZEH):
                        tile = currentCell.getTile((xoffset,yoffset))
                        rendertilecoord = (currentCell.topleft[0]-topleftcoord[0]+xoffset,topleftcoord[1]-currentCell.topleft[1]+yoffset)
                        canvascoord = (rendertilecoord[0]*tilesize[0],rendertilecoord[1]*tilesize[1])
                        color = BIOMECOLORMAP[tile.type]

                        mapCanvas.create_rectangle( [canvascoord[0],
                                                    canvascoord[1],
                                                    canvascoord[0] + tilesize[0],
                                                    canvascoord[1] + tilesize[1]],
                                                    width=0,
                                                    fill=color)


        return

        
BIOMECOLORMAP = {
    WORLDTILETYPES.DESERT: "yellow",
    WORLDTILETYPES.VOID: "black",
    WORLDTILETYPES.FOREST: "green",
    WORLDTILETYPES.OCEAN: "blue",
    WORLDTILETYPES.PLAINS: "#88FF00",
    WORLDTILETYPES.TUNDRA: "#DDDDEE",
    WORLDTILETYPES.MOUNTAIN: "#F4A460",
}


        

