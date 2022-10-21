import ui

class Core:
    """Container for the game object"""

    def __init__(
        self
    ):
        self.ui = ui.GUI()
        self.launch()
        return

    def launch(
        self
    ):
        self.ui.guiStart()