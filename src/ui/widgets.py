import math
import numpy as np
# import matplotlib.pyplot as plt
from scipy import ndimage
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
        charcell = map.findCell((coords[0]-radius,coords[1]+radius))
        topleftcoord = charcell.topleft #this coordinate is mapped to 0,0 on the canvas

        loadedmap = np.zeros((CELLSIZEW*(2*radius+1),CELLSIZEH*(2*radius+1)))
        for celloffsetx in range(charcellcoord[0]-radius,charcellcoord[0]+radius+1):
            for celloffsety in range(charcellcoord[1]-radius,charcellcoord[1]+radius+1):
                land = map.findCell((celloffsetx,celloffsety)).landmap

                loadedmap[CELLSIZEW*(celloffsetx+radius):CELLSIZEW*(celloffsetx+radius+1)-1,
                            CELLSIZEH*(celloffsety+radius):CELLSIZEH*(celloffsety+radius+1)-1] = land

        # fill canvas
        def _photo_image(image: np.ndarray,grey=False):
            height, width = image.shape
            if grey:
                newimage = np.empty((height,width,3))
                newimage[:,:,0] = image*255
                newimage[:,:,1] = image*255
                newimage[:,:,2] = image*255
                image = newimage
            data = f'P6 {width} {height} 255\n'.encode() + newimage.astype(np.uint8).tobytes()

            with open('example.ppm', 'wb') as file:
                file.write(data)
                newimage.tofile(file)

            return tk.PhotoImage(width=width, height=height, data=data, format='PPM')
        img = _photo_image(loadedmap,grey=True)        

        mapCanvas = tk.Canvas(self,width=img.width(),height=img.height(),bg="magenta")
        mapCanvas.pack()
        mapCanvas.create_image(0,0,image=img,tags="image")


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


        

# def printmap(
#     arr:np.ndarray,
#     title=""
# ):
#     # print('\n'.join('  '.join("{:} ".format(int(x)) for x in row) for row in arr.tolist()))
#     plt.figure()
#     plt.title(title)
#     plt.imshow(arr.T,interpolation="none",origin='lower')
#     return