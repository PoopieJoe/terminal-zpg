import math

class CONSTANTOBJECT:
    def contains(self,*args):
        for arg in args:
            if arg not in self.__dict__.values():
                return False
        return True

    def getlist(self):
        return list(self.__dict__.values())


# UI constants
    # Window
SCREENW = 1600
SCREENH = 900


# Gameplay
    # Character
        # Traits
class Classes(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.WARRIOR = "Warrior"
        self.MAGE = "Mage"
        self.BARD = "Bard"
CLASSES = Classes()

class Races(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.HUMAN = "Human"
        self.ELF = "Elf"
        self.DWARF = "Dwarf"
RACES = Races()

class Backgrounds(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.SOLDIER = "Soldier"
        self.ENTERTAINER = "Entertainer"
        self.SCHOLAR = "Scholar"
BACKGROUNDS = Backgrounds()

class CombatStyles(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.MELEE = "Melee"
        self.RANGED = "Ranged"
        self.SPELLS = "Spells"
COMBATSTYLES = CombatStyles()

class Attributes(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.POWER = "Power"
        self.FINESSE = "Finesse"
        self.REASONING = "Reasoning"
        self.WISDOM = "Wisdom"
        self.CHARISMA = "Charisma"
        self.FAITH = "Faith"
ATTRIBUTES = Attributes()

        # Stats
class Stats(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.LIFE = "Life"
        self.STAMINA = "Stamina"
        self.MAGIC = "Magic"
        self.PHYSDMG = "Physical Damage"
        self.MAGDMG = "Magical Damage"
        self.ABILITYSLOTS = "Ability Slots"
        self.PERSUASION = "Persuasion"
        self.LUCK = "Luck"
        self.DEDUCTION = "Deduction"
        self.PRESENCE = "Presence"
        self.CONVICTION = "Conviction"
        self.SLEIGHT = "Sleight"
        self.STEALTH = "Stealth"
        self.SPEED = "Speed"
STATS = Stats()

class BaseStats(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.LIFE = 30
        self.STAMINA = 30
        self.MAGIC = 30
        self.PHYSDMG = 10
        self.MAGDMG = 10
        self.ABILITYSLOTS = 1
        self.PERSUASION = 20
        self.LUCK = 20
        self.DEDUCTION = 20
        self.PRESENCE = 20
        self.CONVICTION = 20
        self.SLEIGHT = 20
        self.STEALTH = 20
        self.SPEED = 20
BASESTATS = BaseStats()

class LevelBonus(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.LIFE = 15
        self.STAMINA = 15
        self.MAGIC = 15
        self.PHYSDMG = 10
        self.MAGDMG = 10
        self.ABILITYSLOTS = 0.5
        self.PERSUASION = 10
        self.LUCK = 10
        self.DEDUCTION = 10
        self.PRESENCE = 10
        self.CONVICTION = 10
        self.SLEIGHT = 10
        self.STEALTH = 10
        self.SPEED = 10
LEVELBONUS = LevelBonus()

class StatModifiers(CONSTANTOBJECT):
    def __init__(self,attrobj:Attributes,statsobj:Stats):
        super().__init__()
        self._columnorder = list(attrobj.__dict__.values())
        self._roworder = list(statsobj.__dict__.values())
        self._modmatrix = [
            [   1,      0,      0,      0,      -0.5,   1],         #Life
            [   1,      1,      -0.5,   0,      0,      0],         #Stamina
            [   -0.5,   0,      1,      1,      0,      0],         #Magic
            [   1,      0,      0,      -0.5,   0,      0],         #Physdmg
            [   0,      0,      1,      -0.5,   0,      0],         #Magdmg
            [   0,      0,      0.1,    0.1,    0,      -0.05],     #Abilityslots
            [   0,      0,      0,      0,      1,      1],         #Persuasion
            [   0,      0,      -0.5,   1,      1,      0],         #Luck
            [   -0.5,   0,      0,      1,      0,      -0.5],      #Deduction
            [   0,      -0.5,   0,      0,      1,      -0.5],      #Presence
            [   0,      -0.5,   0,      0,      0,      1],         #Conviction
            [   -0.5,   1,      0,      0,      0,      0],         #Sleight
            [   -0.5,   1,      0,      0,      0,      0],         #Stealth
            [   0,      1,      0,      0,      -0.5,   0],         #Speed
        ]

    def _getRowNum(self,stat:str):
        return self._roworder.index(stat)

    def _getColNum(self,attribute:str):
        self._columnorder.index(attribute)

    def getVal(self,stat:str,attribute:str):
        column = self._getColNum(attribute)
        row = self._getRowNum(stat)
        return self._modmatrix[row][column]

    def getCol(self,attribute:str):
        column = self._getColNum(attribute)
        return self._modmatrix[:][column]

    def getRow(self,stat:str):
        row = self._getRowNum(stat)
        return self._modmatrix[row][:]
STATMODS = StatModifiers(attrobj=ATTRIBUTES,statsobj=STATS)



    # World
class WindDirections(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.NORTH = "North"
        self.NORTHEAST = "Northeast"
        self.EAST = "East"
        self.SOUTHEAST = "Southeast"
        self.SOUTH = "South"
        self.SOUTHWEAST = "Southwest"
        self.WEST = "West"
        self.NORTHWEST = "Northwest"
WINDDIRECTIONS = WindDirections()

CELLSIZEW = 128
CELLSIZEH = 128
CELLSIZE = (CELLSIZEW,CELLSIZEH)
ORIGINOFFSET = (math.floor(CELLSIZEW/2),math.floor(CELLSIZEH/2))
class WorldTileTypes(CONSTANTOBJECT):
    def __init__(self):
        super().__init__()
        self.VOID = "Void"
        self.PLAINS = "Plains"
        self.FOREST = "Forest"
        self.DESERT = "Desert"
        self.OCEAN = "Ocean"
        self.MOUNTAIN = "Mountain"
        self.TUNDRA = "Tundra"
        self.MOUNTAINPEAK = "Mountain_peak"

WORLDTILETYPES = WorldTileTypes()
WORLDGENTILESBLACKLIST = [
    WORLDTILETYPES.VOID,
    WORLDTILETYPES.MOUNTAINPEAK
]
WORLDGENERATORTILES = [tt for tt in WORLDTILETYPES.getlist() if tt not in WORLDGENTILESBLACKLIST]