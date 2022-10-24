import tkinter as tk
import src.control as control
import src.ui.widgets as widgets
from src.constants import *

class GUI(tk.Tk):
    """Container for the game gui"""
    def __init__(
        self,
        controller:control.Controller
    ):
        tk.Tk.__init__(self)

        self.controller = controller

        self.title("Tk Example")
        self.minsize(200, 200)  # width, height
        self.maxsize(1280, 720)  # width, height
        self.geometry("1280x720+50+50")
        self.config(bg="skyblue")
        self.createWidgets()
        return

    def createWidgets(self):
        """Create the widgets for the frame."""             
        #   Frame Container
        self.rootcontainer = tk.Frame(self)
        self.rootcontainer.grid(row=0, column=0, sticky=tk.W+tk.E)

        #   Frames
        self.frames = {}
        for f in (FrameHome,FrameWorld): # defined subclasses of BaseFrame
            frame = f(self, self.rootcontainer)
            frame.grid(row=2, column=2, sticky=tk.NW+tk.SE)
            frame.config(bg="black")
            self.frames[f] = frame
        self.showFrame(FrameHome)

    def showFrame(self, frameclass):
        self.frames[frameclass].tkraise()

class BaseFrame(tk.Frame):
    """Container for a (sub)menu"""
    def __init__(
        self,
        frameController:GUI,
        master
    ):
        tk.Frame.__init__(self, master)
        self.frameController = frameController
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        """Placeholder that creates the widgets for the frame"""
        return NotImplementedError

class FrameHome(BaseFrame):
    """Home screen"""
    def createWidgets(self):
        top_bar = tk.Frame(self,width=1260,height=30)
        top_bar.grid(row=0,column=0,padx=5,pady=5)

        quit_button = tk.Button(top_bar,text="Quit", command=self.quit)
        quit_button.pack(side="right")

        title_label = tk.Label(top_bar,text="Title")
        title_label.pack(side="left")

        bottom_panel = tk.Frame(self)
        bottom_panel.grid(row=1,column=0)

        main_panel = tk.Frame(bottom_panel,width=900, height=650, bg="grey")
        main_panel.grid(row=1,column=0,padx=10,pady=10)

        log_panel = tk.Frame(main_panel,width=900, height=500, bg="purple")
        log_panel.grid(row=0,column=0,padx=10,pady=10)

        activity_panel = tk.Frame(main_panel,width=900, height=100, bg="purple")
        activity_panel.grid(row=1,column=0,padx=10,pady=10)

        right_panel = tk.Frame(bottom_panel,width=340, height=650, bg="grey")
        right_panel.grid(row=1,column=1,padx=10,pady=10)

        # Name
        name_panel = tk.Frame(right_panel, width=280, height=50, bg="purple")
        name_panel.grid(row=0,column=0,padx=10,pady=10)

        name_label = tk.Label(name_panel,text="Steve")
        name_label.grid(padx=5,pady=5)

        # Attributes
        attr_panel = tk.Frame(right_panel, width=280, height=150, bg="purple")
        attr_panel.grid(row=1,column=0,padx=10,pady=10)

        life_label = tk.Label(attr_panel,text="Life")
        life_label.grid(row=0,column=0,padx=5,pady=5)

        life_bar = tk.Frame(attr_panel,width=200,height=30,bg="red")
        life_bar.grid(row=0,column=1,padx=5,pady=5)

        stamina_label = tk.Label(attr_panel,text="Stamina")
        stamina_label.grid(row=1,column=0,padx=5,pady=5)

        stamina_bar = tk.Frame(attr_panel,width=200,height=30,bg="green")
        stamina_bar.grid(row=1,column=1,padx=5,pady=5)

        magic_label = tk.Label(attr_panel,text="Magic")
        magic_label.grid(row=2,column=0,padx=5,pady=5)

        magic_bar = tk.Frame(attr_panel,width=200,height=30,bg="blue")
        magic_bar.grid(row=2,column=1,padx=5,pady=5)

        # Status
        status_panel = tk.Frame(right_panel, width=280, height=50, bg="purple")
        status_panel.grid(row=2,column=0,padx=10,pady=10)

        status_label = tk.Label(status_panel,text="Status")
        status_label.grid(row=0,column=0,padx=5,pady=5)

        # abilities+equipment
        abilityequipment_panel = tk.Frame(right_panel, width=280, height=300, bg="purple")
        abilityequipment_panel.grid(row=3,column=0,padx=10,pady=10)

        # Abilities
        ability_panel = tk.Frame(abilityequipment_panel, width=120, height=300, bg="yellow")
        ability_panel.grid(row=0,column=0,padx=10,pady=10)

        # Equipment
        equipment_panel = tk.Frame(abilityequipment_panel, width=120, height=300, bg="yellow")
        equipment_panel.grid(row=0,column=1,padx=10,pady=10)

class FrameWorld(BaseFrame):
    """Shows worldgen map"""
    def createWidgets(self):
        world = self.frameController.controller.newworld
        map = widgets.MapRenderer(self,world,(0,0))
        print(map)


