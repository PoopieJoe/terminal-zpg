import json
from src.constants import *
from numpy import dot

class Character:
    def __init__(
        self,
    ):
        return

    def importFromJSON(
        self,
        src
    ):
        #TODO
        return

    def exportToJSON(
        self
    ):
        #TODO
        return

    def generate(
        self,
        name = None,
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
        self.maxLife = BASESTATS.LIFE + level*LEVELBONUS.LIFE + dot(attributearr,STATMODS.getRow(STATS.LIFE))
        self.maxStamina = BASESTATS.STAMINA + level*LEVELBONUS.STAMINA + dot(attributearr,STATMODS.getRow(STATS.STAMINA))
        self.maxMagic = BASESTATS.MAGIC + level*LEVELBONUS.MAGIC + dot(attributearr,STATMODS.getRow(STATS.MAGIC))
        self.physDmg = BASESTATS.PHYSDMG + level*LEVELBONUS.PHYSDMG + dot(attributearr,STATMODS.getRow(STATS.PHYSDMG))
        self.magDmg = BASESTATS.MAGDMG + level*LEVELBONUS.MAGDMG + dot(attributearr,STATMODS.getRow(STATS.MAGDMG))
        self.abilitySlots = BASESTATS.ABILITYSLOTS + level*LEVELBONUS.ABILITYSLOTS + dot(attributearr,STATMODS.getRow(STATS.ABILITYSLOTS))
        self.persuasion = BASESTATS.PERSUASION + level*LEVELBONUS.PERSUASION + dot(attributearr,STATMODS.getRow(STATS.PERSUASION))
        self.luck = BASESTATS.LUCK + level*LEVELBONUS.LUCK + dot(attributearr,STATMODS.getRow(STATS.LUCK))
        self.deduction = BASESTATS.DEDUCTION + level*LEVELBONUS.DEDUCTION + dot(attributearr,STATMODS.getRow(STATS.DEDUCTION))
        self.presence = BASESTATS.PRESENCE + level*LEVELBONUS.PRESENCE + dot(attributearr,STATMODS.getRow(STATS.PRESENCE))
        self.conviction = BASESTATS.CONVICTION + level*LEVELBONUS.CONVICTION + dot(attributearr,STATMODS.getRow(STATS.CONVICTION))
        self.sleight = BASESTATS.SLEIGHT + level*LEVELBONUS.SLEIGHT + dot(attributearr,STATMODS.getRow(STATS.SLEIGHT))
        self.stealth = BASESTATS.STEALTH + level*LEVELBONUS.STEALTH + dot(attributearr,STATMODS.getRow(STATS.STEALTH))
        self.speed = BASESTATS.SPEED + level*LEVELBONUS.SPEED + dot(attributearr,STATMODS.getRow(STATS.SPEED))

        

        return
