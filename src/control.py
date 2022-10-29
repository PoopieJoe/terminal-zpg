from numpy import identity
import src.character as char
import src.world as world

class Controller:
    def __init__(
        self
    ):
        self.world = world.World()

        pc = char.Character()
        pc.generate()

        self.entities = []

        # place character in world
        self.addEntity("PC",(0,0),pc)
        return

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
        self
    ):
        for entity in self.entities:
            entity.update()

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