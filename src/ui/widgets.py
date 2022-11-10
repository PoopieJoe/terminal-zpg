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

        loadedmap = np.zeros((CELLSIZEW*(2*radius+1),CELLSIZEH*(2*radius+1)))
        for celloffsetx in range(int(charcellcoord[0]-radius),int(charcellcoord[0]+radius+1)):
            for celloffsety in range(int(charcellcoord[1]-radius),int(charcellcoord[1]+radius+1)):
                land = map.findCell((celloffsetx,celloffsety)).heightmap

                loadedmap[CELLSIZEW*(celloffsetx+radius):CELLSIZEW*(celloffsetx+radius+1)-1,
                            CELLSIZEH*(celloffsety+radius):CELLSIZEH*(celloffsety+radius+1)-1] = land

        # image containing all chunks
        self.img = Image.fromarray(loadedmap/loadedmap.max()*255)#_numpy2ppm(self,loadedmap/loadedmap.max()*255,"example.ppm")#

        # fetch rendered rectangle
        rectsz = (600,600)
        rectpos = (0,0)
        rect = (rectpos[0],rectpos[1],rectpos[0]+rectsz[0],rectpos[1]+rectsz[1])

        self.img = self.img.crop(rect)
        self.pimg = ImageTk.PhotoImage(self.img,master=self)
        self.create_image(0,0,anchor=tk.NW,image=self.pimg)
        
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