import math
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

import src.world as world
from src.constants import *


class MapRenderer(tk.Canvas):
    def __init__(
        self,
        master,
        map:world.World,
        coords:tuple
    ):
        tk.Canvas.__init__(self,master=master,width=600,height=600)
        renderareasize = 3      # render area size in chunks (3x3)
        radius = math.floor(renderareasize/2) # load relevant chunks
        charcellcoord,tileoffset = map.coords2cellOffset(coords)   # chunk of character

        self.loadedcells = []
        self.loadedmap = np.zeros((CELLSIZEW*(2*radius+1),CELLSIZEH*(2*radius+1)))
        for celloffsetx in range(int(charcellcoord[0]-radius),int(charcellcoord[0]+radius+1)):
            for celloffsety in range(int(charcellcoord[1]-radius),int(charcellcoord[1]+radius+1)):
                cell = map.findCell((celloffsetx,celloffsety))
                self.loadedcells.append(cell)
                land = cell.heightmap

                self.loadedmap[CELLSIZEW*(celloffsetx+radius):CELLSIZEW*(celloffsetx+radius+1)-1,
                            CELLSIZEH*(celloffsety+radius):CELLSIZEH*(celloffsety+radius+1)-1] = land

        # image containing all chunks
        self.img = Image.fromarray(self.loadedmap/self.loadedmap.max()*255)

        # fetch rendered rectangle
        # centered around pc in center cell
        # will always be within the centre third
        rectsz = (600,600)
        rectpos = (CELLSIZEW+tileoffset[0]/renderareasize/2,CELLSIZEH+tileoffset[1]/renderareasize/2)
        rect = (int(rectpos[0]),int(rectpos[1]),int(rectpos[0]+rectsz[0]),int(rectpos[1]+rectsz[1]))

        self.img = self.img.crop(rect)
        self.img = ImageTk.PhotoImage(self.img,master=self)
        self.create_image(0,0,anchor=tk.NW,image=self.img)
        
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


#EXAMPLE: _numpy2ppm(self,loadedmap/loadedmap.max()*255,"example.ppm")#
# def _numpy2ppm(canvas:tk.Canvas,image: np.ndarray,export=None):
#     """Convert np array to PPM formatted image\n
#         image: N-dimensional array of shape (width,height) for greyscale OR (width,height,3) for RGB-255"""
#     if len(image.shape) == 3:
#         height, width, depth = image.shape
#         if depth > 3:
#             raise ValueError("Too many color channels, only RGB allowed")
#     elif len(image.shape) == 2:
#         height, width = image.shape
#         newimage = np.empty((height,width,3))
#         newimage[:,:,0] = image
#         newimage[:,:,1] = image
#         newimage[:,:,2] = image
#         image = newimage
#     else:
#         raise ValueError("Image shape must be (wxh) or (wxhxd)")

#     data = f'P6 {width} {height} 255\n'.encode() + image.astype(np.uint8).tobytes()
#     if export != None:
#         with open(export, 'wb') as file:
#             file.write(data)
#             newimage.tofile(file)
#             print("Exported to image: "+export)
#     return tk.PhotoImage(master=canvas,data=data, format='ppm')