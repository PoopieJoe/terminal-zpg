import math
import numpy as np
# import matplotlib.pyplot as plt
from scipy import ndimage
import tkinter as tk
import src.control as control
import src.cell as cell
from PIL import Image,ImageTk
import src.world as world
from src.constants import *

class MapRenderer(tk.Label):
    def __init__(
        self,
        master,
        map:world.World,
        coords:tuple
    ):
        
        tk.Label.__init__(self,master=master,text="hoi")
        framew = SCREENW
        frameh = SCREENH    
        framesize = min(frameh,framew) # take minimum to be square
        renderareasize = 3      # render area size in chunks (3x3)
        
        tilesize = (math.floor(framesize/(renderareasize*CELLSIZEW)),math.floor(framesize/(renderareasize*CELLSIZEH)))            # size of a tile in px
        width = renderareasize*CELLSIZEW*tilesize[0]
        height = renderareasize*CELLSIZEH*tilesize[1]

        # load relevant chunks (3x3 centered around character)
        radius = math.floor(renderareasize/2)
        charcellcoord,tileoffset = map.coords2cellOffset(coords)   # chunk of character
        # charcell = map.findCell((coords[0]-radius,coords[1]+radius))
        # topleftcoord = charcell.topleft #this coordinate is mapped to 0,0 on the canvas

        loadedmap = np.zeros((CELLSIZEW*(2*radius+1),CELLSIZEH*(2*radius+1)))
        for celloffsetx in range(charcellcoord[0]-radius,charcellcoord[0]+radius+1):
            for celloffsety in range(charcellcoord[1]-radius,charcellcoord[1]+radius+1):
                land = map.findCell((celloffsetx,celloffsety)).heightmap

                loadedmap[CELLSIZEW*(celloffsetx+radius):CELLSIZEW*(celloffsetx+radius+1)-1,
                            CELLSIZEH*(celloffsety+radius):CELLSIZEH*(celloffsety+radius+1)-1] = land

        # fill canvas
        self.img = ImageTk.PhotoImage(Image.fromarray(loadedmap/loadedmap.max()*255),master=self)#_numpy2ppm(self,loadedmap/loadedmap.max()*255,"example.ppm")#
        
        self.configure(image=self.img)
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

def _numpy2ppm(canvas:tk.Canvas,image: np.ndarray,export=None):
    """Convert np array to PPM formatted image\n
        image: N-dimensional array of shape (width,height) for greyscale OR (width,height,3) for RGB-255"""
    if len(image.shape) == 3:
        height, width, depth = image.shape
        if depth > 3:
            raise ValueError("Too many color channels, only RGB allowed")
    elif len(image.shape) == 2:
        height, width = image.shape
        newimage = np.empty((height,width,3))
        newimage[:,:,0] = image
        newimage[:,:,1] = image
        newimage[:,:,2] = image
        image = newimage
    else:
        raise ValueError("Image shape must be (wxh) or (wxhxd)")

    data = f'P6 {width} {height} 255\n'.encode() + image.astype(np.uint8).tobytes()
    if export != None:
        with open(export, 'wb') as file:
            file.write(data)
            newimage.tofile(file)
            print("Exported to image: "+export)
    return tk.PhotoImage(master=canvas,data=data, format='ppm')