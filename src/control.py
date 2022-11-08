import time
import os
import src.character as char
import src.world as world
import src.saveload as saveload
import src.taskmanager as tsk
from src.constants import *

class Controller:
    def __init__(
        self
    ):
        self.worlds = {}
        self.entities = {}

        self.name = input("Give world name: ")

        # check if file exists already in SAVEFOLDER
        if os.path.exists(saveload.savefilePath(self.name)):
            print("World found! Loading from file...")
            self.importCurrentGame(self.name)
        else:
            print("World not found, creating new...")
            self.seed = input("Give world seed [<Enter> to use world name]: ")
            if self.seed == "":
                self.seed = self.name

            print("Generating Overworld...")
            overworld = world.World(OVERWORLDNAME,self.seed)
            overworld.generate()
            self.addWorld({overworld.name:overworld})

            print("Generating character...")
            pc = char.Character()
            pc.generate()
            self.addEntity("PC",(0,0),pc)

            act = tsk.Activity("Walk","something",destination = "should be an entity or tile coordinate")
            task = tsk.Task("Go to place",subtasks={act},description = "Testdescr")
            self.giveTask(self.entities[0],task)

            self.t_ns = 0

            print("Saving to file...")
            self.exportCurrentGame()
        print("Done")

        # create task and activities


        return

    def exportCurrentGame(
        self
    ):
        outputobj = {}
        for key in SAVEKEYS:
            outputobj[key] = self.__dict__[key]
        saveload.saveToJSON(outputobj,filename=self.name)
        return

    def importCurrentGame(
        self,
        filename
    ):
        inputobj = saveload.loadFromJSON(filename=filename)
        for key in SAVEKEYS:
            self.__dict__[key] = inputobj[key]

    def addWorld(
        self,
        world:world.World
    ):
        self.worlds.update(world)

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
        newentity = Entity(_id,type,pos,entity,updatef)
        self.entities.update({_id:newentity})
        return _id

    def giveTask(
        self,
        entity,
        task,
        supertask = None
    ):
        if entity in self.entities.values():
            entity.object.addTask(task,supertask)
            print("Added task <" + task.name + "> to entity <" + entity.id + ">")
        else:
            print("Failed to add task <" + task.name + "> to entity <id=" + entity + ">. Entity does not exist.")
            return False

    def update( # run one update for all applicable characters and tiles
        self,
        dt_ns # time since last update in ns
    ):
        self.t_ns += dt_ns
        ns2s = lambda t : t/1000000000
        ns2ms = lambda t : t/1000000
        

        print("[{:06.2f}] Time since last update: {:07.2f}ms".format(ns2s(self.t_ns),ns2ms(dt_ns)))
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