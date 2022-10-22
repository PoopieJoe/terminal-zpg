import src.ui
import src.control

class Core:
    """Container for the game object"""

    def __init__(
        self
    ):
        self.ui = src.ui.GUI()
        self.controller = src.control.Controller()
        return

    def launch(
        self
    ):
        self.ui.guiStart()