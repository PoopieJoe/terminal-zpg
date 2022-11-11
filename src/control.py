import time
import os
import src.entities as ent
import src.world as world
import src.saveload as saveload
import src.taskmanager as tsk
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
            self.importCurrentGame(self.name)
        else:
            print("World not found, creating new...")
            self.seed = input("Give world seed [<Enter> to use world name]: ")
            if self.seed == "":
                self.seed = self.name

            print("Generating Overworld...")
            overworld = world.World(OVERWORLDNAME,self.seed)
            overworld.generate()
            self.addWorld(overworld)

            print("Generating character...")
            
            self.pc = self.addEntity(ent.PlayerCharacter,[0,0])
            self.pc.generate()

            task = tsk.Task(self.pc.taskmanager,"Go to place",description = "Testdescr")
            act = tsk.GotoActivity(self.pc.taskmanager,task=task,destination = (10,10))
            act1 = tsk.GotoActivity(self.pc.taskmanager,task=task,destination = (10,-10))
            act2 = tsk.GotoActivity(self.pc.taskmanager,task=task,destination = (-10,0))
            self.pc.addTask(task)

            self.t_ns = 0

            print("Saving to file...")
            self.exportCurrentGame()
        print("Done")
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
        self.worlds.append(world)

    def addEntity(
        self,
        _c,
        pos
    ):
        _id = 0
        while ( _id in [e.id for e in self.entities] 
                and self.entities != []):
            _id = _id + 1
        print("Added entity: " + str(_c) + " at " + str(pos))
        newentity = _c(self,_id,pos)
        self.entities.append(newentity)
        return newentity

    def giveTask(
        self,
        entity,
        task,
        supertask = None
    ):
        if entity in self.entities:
            entity.addTask(task,supertask)
            print("Added task <" + task.name + "> to entity <" + str(entity.id) + ">")
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
        
        os.system('cls' if os.name == 'nt' else 'clear') # clear terminal each update

        print("[{:06.2f}] Time since last update: {:07.2f}ms".format(ns2s(self.t_ns),ns2ms(dt_ns)))
        for entity in self.entities:
            entity.update(dt=ns2s(dt_ns))
        return
