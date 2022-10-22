import src.character as char

class Controller:
    def __init__(
        self
    ):
        newchar = char.Character()
        newchar.generate()
        print(newchar)
        return