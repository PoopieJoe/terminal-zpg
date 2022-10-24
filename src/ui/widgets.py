import tkinter as tk
import src.control as control
import src.world as world

class MapRenderer(tk.Frame):
    def __init__(
        self,
        master,
        world:world.World,
        coords:tuple
    ):
        tk.Frame(master)

