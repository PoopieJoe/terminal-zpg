import src.ui.ui as ui
import src.control as control

class Core:
    """Container for the game object"""

    def __init__(
        self
    ):
        self.controller = control.Controller()
        self.ui = ui.GUI(self.controller)
        
        return

    def launch(
        self
    ):
        self.ui.mainloop()