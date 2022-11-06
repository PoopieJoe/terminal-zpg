import time
import os
import src.character as char
import src.world as world
import src.saveload as saveload
from src.constants import *

class Controller:
    def __init__(
        self
    ):
        self.worlds = []
        self.entities = []

        self.name = input("Give world name: ")

        # check if file exists already in SAVEFOLDER
        if os.path.exists(saveload.savefilePath(self.name)):
            print("World found! Loading from file...")
            inputobj = saveload.loadFromJSON(filename=self.name)
            for key in SAVEKEYS:
                self.__dict__[key] = inputobj[key]
        else:
            print("World not found, creating new...")
            self.seed = input("Give world seed [<Enter> to use world name]: ")
            if self.seed == "":
                self.seed = self.name

            print("Generating Overworld...")
            overworld = world.World("overworld",self.seed)
            overworld.generate()
            self.addWorld(overworld)

            print("Generating character...")
            pc = char.Character()
            pc.generate()
            self.addEntity("PC",(0,0),pc)

            print("Saving to file...")
            outputobj = {}
            for key in SAVEKEYS:
                outputobj[key] = self.__dict__[key]
            saveload.saveToJSON(outputobj,filename=self.name)
        print("Done")
        return

    def addWorld(
        self,
        world:world.World
    ):
        self.worlds.append(world)

    def addEntity(
        self,
        type,
        pos,
        entity,
        updatef = None
    ):
        _id = 0
        while ( _id in [e.id for e in self.entities] 
                and self.entities != []):
            _id = _id + 1
        print("Added entity: " + str(type) + " at " + str(pos))
        self.entities.append(Entity(_id,type,pos,entity,updatef))
    
    def update( # run one update for all applicable characters and tiles
        self,
        t_ns, # time since start of world in ns
        dt_ns # time since last update in ns
    ):
        ns2s = lambda t : t/1000000000
        ns2ms = lambda t : t/1000000

        print("[{:.2f}] Time since last update: {:.2f}ms".format(ns2s(t_ns),ns2ms(dt_ns)))
        # for entity in self.entities:
        #     entity.update()
        return

class Entity:
    def __init__(
        self,
        type,
        id,
        pos,
        object,
        updatef = None
    ):
        self.id = id
        self.type = type
        self.pos = pos
        self.object = object
        self._updatef = updatef
    
    def update(
        self,
        *arg,
        **kwargs
    ):
        return self._updatef(*arg,**kwargs)