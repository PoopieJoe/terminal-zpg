import os
import datetime
from src.constants import *

class Logger:
    def __init__(
        self,
        controller
    ):
        self.controller = controller
        if not os.path.isdir(LOGSFOLDERPATH):
            os.makedirs(LOGSFOLDERPATH)
        return

    def open(
        self
    ):
        with open(EVTLOGFILEPATH, "w") as file:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write("Event log started on: {}\n".format(now))
        return

    def close(
        self
    ):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(EVTLOGFILEPATH, "a") as file:
            file.write("Event log closed on: {}\n".format(now))
        return

    def getheader(
        self
    ):
        return "[{:06.3f}] ".format(self.controller.t_ns/(1*10**9))

    def write(
        self,
        string
    ):
        header = self.getheader()
        with open(EVTLOGFILEPATH, "a") as file:
            file.write(header+string)
        return