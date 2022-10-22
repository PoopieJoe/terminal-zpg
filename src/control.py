import src.character as char
import src.world as world

class Controller:
    def __init__(
        self
    ):
        newchar = char.Character()
        newchar.generate()
        
        newworld = world.World()
        newworld.generate()
        return