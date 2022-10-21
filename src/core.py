import src.ui as ui
import src.control as control

class Core:
    """Container for the game object"""

    def __init__(
        self
    ):
        self.ui = ui.GUI()
        self.controller = control.Controller()
        self.launch()
        return

    def launch(
        self
    ):
        self.ui.guiStart()