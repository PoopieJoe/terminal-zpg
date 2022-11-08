import jsonpickle
import os
import jsonpickle.ext.numpy as jsonpickle_numpy
from src.constants import *

jsonpickle_numpy.register_handlers()



def savefilePath(filename):
    return SAVEFOLDER + filename + "." + SAVEFORMAT

def saveToJSON(obj,filename):
    if not os.path.exists(SAVEFOLDER):
        os.makedirs(SAVEFOLDER)
    with open(savefilePath(filename),'w') as outfile:
        jsonStr = jsonpickle.encode(obj,indent=4)
        outfile.write(jsonStr)
    return

def loadFromJSON(filename):
    with open(savefilePath(filename),'r') as infile:
        jsonStr = infile.read()
        return jsonpickle.decode(jsonStr)