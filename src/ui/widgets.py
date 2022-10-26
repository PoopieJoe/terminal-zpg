import math
import tkinter as tk
from turtle import bgcolor
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
        tilesize = 100         # size of a tile in px
        renderareasize = 3    # render area size in chunks (3x3)
        mapCanvas = tk.Canvas(self,width=tilesize*renderareasize,height=tilesize*renderareasize,bg="white")
        mapCanvas.pack()

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
                        rendertilecoord = (topleftcoord[0]-cell.topleft[0]+xoffset,topleftcoord[1]-cell.topleft[1]+yoffset)
                        canvascoord = (rendertilecoord[0]*tilesize,rendertilecoord[1]*tilesize)
                        match tile.type[0]:
                            case WORLDTILETYPES.VOID:
                                color = "black"#"#000000"
                            case WORLDTILETYPES.FOREST:
                                color = "green"#"#00FF00"
                            case WORLDTILETYPES.DESERT:
                                color = "yellow"
                            case WORLDTILETYPES.OCEAN:
                                color = "blue"
                            case WORLDTILETYPES.PLAINS:
                                color = "#88FF00"
                        mapCanvas.create_rectangle( [canvascoord[0],
                                                    canvascoord[1],
                                                    canvascoord[0] + tilesize,
                                                    canvascoord[1] + tilesize],
                                                    fill=color)
                        renderarea[rendertilecoord[0]][rendertilecoord[1]] = tile

        return

        
        


        

