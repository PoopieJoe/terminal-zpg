import src.ui.ui as ui
import src.control as control
import src.log

class Core:
    """Container for the game object"""

    def __init__(
        self
    ):
        self.controller = control.Controller(self)
        self.logger = src.log.Logger(self.controller)
        self.ui = ui.GUI(self.controller)
        
        self.logger.open()
        return

    def launch(
        self
    ):
        self.ui.mainloop()

    def exit(
        self
    ):
        self.ui.quit()
        self.logger.close()