import src.character as char
import src.world as world

class Controller:
    def __init__(
        self
    ):
        self.newchar = char.Character()
        self.newchar.generate()
        
        self.newworld = world.World()
        self.newworld.generateInitial()
        return