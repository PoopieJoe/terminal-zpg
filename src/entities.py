import json
from src.constants import *
import src.taskmanager as tsk
from numpy import dot

class Entity:
    def __init__(
        self,
        controller,
        id,
        pos
    ):
        self.controller = controller
        self.id = id
        self.pos = pos
        self.vel = [0,0]
    
    def update(
        self,
        **p
    ):
        raise NotImplementedError

class PlayerCharacter(Entity):
    def __init__(
        self,
        controller,
        id,
        pos
    ):
        Entity.__init__(self,controller,id,pos)
        self._state = PCSTATES.IDLE
        return

    def addTask(
        self,
        task:tsk.Task,
        supertask:tsk.Task = None
    ):
        if supertask != None:
            supertask.addsubtask(task)
        else:
            self.tasks.update({task.name:task})

    def _print(
        self,
        s
    ):
        PREFIX = "<Entity {:n} \"{}\" ({:.2f},{:.2f})>: ".format(self.id,self.name,self.pos[0],self.pos[1])
        print(PREFIX + s)

    def update(self, **p):

        # fsm
        if self._state == PCSTATES.IDLE:
            self._print("Doing nothing ...")
        else:
            pass


        # discrete state update
        self.pos[0] += self.vel[0]*p["dt"]
        self.pos[1] += self.vel[1]*p["dt"]

        # check if tasks completed
        return

    def generate(
        self,
        name = "New",
        level = 1,
        power = 10,
        finesse = 10,
        reasoning = 10,
        wisdom = 10,
        charisma = 10,
        faith = 10,
        charclass = None,
        race = None,
        background = None,
        age = None,
        combatStyle = None,
        likes = None,
        dislikes = None
    ):
        self.name = name
        self.level = level

        self.tasks = {}


        #statstuff
        self.power = power
        self.finesse = finesse
        self.reasoning = reasoning
        self.wisdom = wisdom
        self.charisma = charisma
        self.faith = faith

        self.charclass = charclass
        self.race = race
        self.background = background
        self.age = age
        self.combatStyle = combatStyle
        self.likes = likes
        self.dislikes = dislikes

        attributearr = [self.power,self.finesse,self.reasoning,self.wisdom,self.charisma,self.faith]
        self.maxLife        = int(BASESTATS.LIFE            + level*LEVELBONUS.LIFE             + dot(attributearr,STATMODS.getRow(STATS.LIFE)))
        self.maxStamina     = int(BASESTATS.STAMINA         + level*LEVELBONUS.STAMINA          + dot(attributearr,STATMODS.getRow(STATS.STAMINA)))
        self.maxMagic       = int(BASESTATS.MAGIC           + level*LEVELBONUS.MAGIC            + dot(attributearr,STATMODS.getRow(STATS.MAGIC)))
        self.physDmg        = int(BASESTATS.PHYSDMG         + level*LEVELBONUS.PHYSDMG          + dot(attributearr,STATMODS.getRow(STATS.PHYSDMG)))
        self.magDmg         = int(BASESTATS.MAGDMG          + level*LEVELBONUS.MAGDMG           + dot(attributearr,STATMODS.getRow(STATS.MAGDMG)))
        self.abilitySlots   = int(BASESTATS.ABILITYSLOTS    + level*LEVELBONUS.ABILITYSLOTS     + dot(attributearr,STATMODS.getRow(STATS.ABILITYSLOTS)))
        self.persuasion     = int(BASESTATS.PERSUASION      + level*LEVELBONUS.PERSUASION       + dot(attributearr,STATMODS.getRow(STATS.PERSUASION)))
        self.luck           = int(BASESTATS.LUCK            + level*LEVELBONUS.LUCK             + dot(attributearr,STATMODS.getRow(STATS.LUCK)))
        self.deduction      = int(BASESTATS.DEDUCTION       + level*LEVELBONUS.DEDUCTION        + dot(attributearr,STATMODS.getRow(STATS.DEDUCTION)))
        self.presence       = int(BASESTATS.PRESENCE        + level*LEVELBONUS.PRESENCE         + dot(attributearr,STATMODS.getRow(STATS.PRESENCE)))
        self.conviction     = int(BASESTATS.CONVICTION      + level*LEVELBONUS.CONVICTION       + dot(attributearr,STATMODS.getRow(STATS.CONVICTION)))
        self.sleight        = int(BASESTATS.SLEIGHT         + level*LEVELBONUS.SLEIGHT          + dot(attributearr,STATMODS.getRow(STATS.SLEIGHT)))
        self.stealth        = int(BASESTATS.STEALTH         + level*LEVELBONUS.STEALTH          + dot(attributearr,STATMODS.getRow(STATS.STEALTH)))
        self.speed          = int(BASESTATS.SPEED           + level*LEVELBONUS.SPEED            + dot(attributearr,STATMODS.getRow(STATS.SPEED)))
        return