import math
import tkinter as tk
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

        # empty canvas
        canvassize = 700        # size of map canvas in px (NxN)
        renderareasize = 3      # render area size in chunks (3x3)
        tilesize = math.floor(canvassize/(renderareasize*CELLSIZEH))  # size of a tile in px
        mapCanvas = tk.Canvas(self,width=CELLSIZEW*tilesize*renderareasize,height=CELLSIZEH*tilesize*renderareasize,bg="white")
        mapCanvas.pack()

        # load relevant chunks (3x3 centered around character)
        radius = math.floor(renderareasize/2)
        charchunk,tileoffset = map.coords2cellOffset(coords)   # chunk of character

        renderarea = [[cell.Tile(WORLDTILETYPES.VOID) for _ in range(renderareasize*CELLSIZEW)] for _ in range(renderareasize*CELLSIZEH)]

        topleftcoord = map.findCell((coords[0]-radius,coords[1]+radius)).topleft #this coordinate is mapped to 0,0 on the canvas

        for celloffsetx in range(charchunk[0]-radius,charchunk[0]+radius+1):
            for celloffsety in range(charchunk[1]-radius,charchunk[1]+radius+1):
                currentCell = map.findCell((celloffsetx,celloffsety))

                for xoffset in range(CELLSIZEW):
                    for yoffset in range(CELLSIZEH):
                        tile = currentCell.getTile((xoffset,yoffset))
                        rendertilecoord = (currentCell.topleft[0]-topleftcoord[0]+xoffset,topleftcoord[1]-currentCell.topleft[1]+yoffset)
                        canvascoord = (rendertilecoord[0]*tilesize,rendertilecoord[1]*tilesize)
                        color = BIOMECOLORMAP[tile.type]

                        mapCanvas.create_rectangle( [canvascoord[0],
                                                    canvascoord[1],
                                                    canvascoord[0] + tilesize,
                                                    canvascoord[1] + tilesize],
                                                    fill=color)
                        #mapCanvas.create_text(canvascoord[0]+tilesize/2,canvascoord[1]+tilesize/2,text="("+str(xoffset)+"," +str(yoffset)+ ")" )


        return

        
BIOMECOLORMAP = {
    WORLDTILETYPES.DESERT: "yellow",
    WORLDTILETYPES.VOID: "black",
    WORLDTILETYPES.FOREST: "green",
    WORLDTILETYPES.OCEAN: "blue",
    WORLDTILETYPES.PLAINS: "#88FF00",
    WORLDTILETYPES.TUNDRA: "#BBBBBB",
    WORLDTILETYPES.MOUNTAIN: "#F4A460",
}


        

