import tkinter as tk
import time
import copy
import src.control as control
import src.ui.widgets as widgets
import src.ui.events as events
from src.constants import *

class GUI(tk.Tk):
    """Container for the game gui"""
    def __init__(
        self,
        controller:control.Controller
    ):
        tk.Tk.__init__(self)

        self.controller = controller

        self.title("ZPG-RPG")
        self.minsize(480, 360)  # width, height
        self.maxsize(SCREENW, SCREENH)  # width, height
        self.config(bg="magenta")
        self.createFrames()

        #set window in focus
        self.focus_set()
        self.focus_force()
    
        self.tick(time.time_ns())
        return

    def tick(
        self,
        _tnsSinceEpoch
    ):
        dt = time.time_ns() - _tnsSinceEpoch
        _tnsSinceEpoch += dt
        self.controller.update(dt)
        self.nextaftercall = self.after(int(1000/TICKRATE),self.tick,_tnsSinceEpoch)

    def createFrames(self):
        """Create the frames for the ui."""             
        #   Frame Container
        self.rootcontainer = tk.Frame(self,width=SCREENW,height=SCREENH)
        self.bindEvents()
        self.rootcontainer.grid(row=0, column=0, sticky=tk.W+tk.E)

        #   Frames
        self.frames = {}
        for f in (FrameHome,FrameWorld): # defined subclasses of BaseFrame
            frame = f(frameController=self, master=self.rootcontainer)
            frame.grid(row=0, column=0, sticky=tk.NW+tk.SE)
            frame.config(bg="black")
            self.frames[f] = frame
        self.showFrame(FrameHome)

    def showFrame(self, frameclass):
        self.frames[frameclass].tkraise()

    def exit(self,save=False):
        self.after_cancel(self.nextaftercall)
        self.destroy()
        if save:
            print("Saving and quitting...")
            self.controller.exportCurrentGame()
        else:
            print("Quitting...")
        self.quit()

    def bindEvents(
        self
    ):  
        self.bind("<KeyPress-Up>",events.onUpArrowPress)
        self.bind("<KeyRelease-Up>",events.onUpArrowRelease)
        self.bind("<KeyPress-Down>",events.onDownArrowPress)
        self.bind("<KeyRelease-Down>",events.onDownArrowRelease)
        self.bind("<KeyPress-Left>",events.onLeftArrowPress)
        self.bind("<KeyRelease-Left>",events.onLeftArrowRelease)
        self.bind("<KeyPress-Right>",events.onRightArrowPress)
        self.bind("<KeyRelease-Right>",events.onRightArrowRelease)
        return
        

class BaseFrame(tk.Frame):
    """Container for a (sub)menu"""
    def __init__(
        self,
        frameController:GUI,
        master
    ):
        tk.Frame.__init__(self, master,width=SCREENW,height=SCREENH)
        self.frameController = frameController
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        """Placeholder that creates the widgets for the frame"""
        return NotImplementedError

class FrameHome(BaseFrame):
    """Home screen"""
    def createWidgets(self):
        self.top_bar = tk.Frame(self,width=SCREENW-20,height=SCREENH-20)
        self.top_bar.grid(row=0,column=0,padx=5,pady=5)

        self.quit_button = tk.Button(self.top_bar,text="Save and quit", command=lambda: self.frameController.exit(save=True))
        self.quit_button.grid(row=0,column=2)

        self.map_button = tk.Button(self.top_bar,text="Switch to map view",command=lambda: self.frameController.showFrame(FrameWorld))
        self.map_button.grid(row=0,column=1)

        self.title_label = tk.Label(self.top_bar,text="Title")
        self.title_label.grid(row=0,column=0)

        self.bottom_panel = tk.Frame(self)
        self.bottom_panel.grid(row=1,column=0)

        self.main_panel = tk.Frame(self.bottom_panel,width=900, height=650, bg="grey")
        self.main_panel.grid(row=1,column=0,padx=10,pady=10)

        self.log_panel = tk.Frame(self.main_panel,width=900, height=500, bg="purple")
        self.log_panel.grid(row=0,column=0,padx=10,pady=10)

        self.activity_panel = tk.Frame(self.main_panel,width=900, height=100, bg="purple")
        self.activity_panel.grid(row=1,column=0,padx=10,pady=10)

        self.right_panel = tk.Frame(self.bottom_panel,width=340, height=650, bg="grey")
        self.right_panel.grid(row=1,column=1,padx=10,pady=10)

        # Name
        self.name_panel = tk.Frame(self.right_panel, width=280, height=50, bg="purple")
        self.name_panel.grid(row=0,column=0,padx=10,pady=10)

        self.name_label = tk.Label(self.name_panel,text="Steve")
        self.name_label.grid(padx=5,pady=5)

        # Attributes
        self.attr_panel = tk.Frame(self.right_panel, width=280, height=150, bg="purple")
        self.attr_panel.grid(row=1,column=0,padx=10,pady=10)

        self.life_label = tk.Label(self.attr_panel,text="Life")
        self.life_label.grid(row=0,column=0,padx=5,pady=5)

        self.life_bar = tk.Frame(self.attr_panel,width=200,height=30,bg="red")
        self.life_bar.grid(row=0,column=1,padx=5,pady=5)

        self.stamina_label = tk.Label(self.attr_panel,text="Stamina")
        self.stamina_label.grid(row=1,column=0,padx=5,pady=5)

        self.stamina_bar = tk.Frame(self.attr_panel,width=200,height=30,bg="green")
        self.stamina_bar.grid(row=1,column=1,padx=5,pady=5)

        self.magic_label = tk.Label(self.attr_panel,text="Magic")
        self.magic_label.grid(row=2,column=0,padx=5,pady=5)

        self.magic_bar = tk.Frame(self.attr_panel,width=200,height=30,bg="blue")
        self.magic_bar.grid(row=2,column=1,padx=5,pady=5)

        # Status
        self.status_panel = tk.Frame(self.right_panel, width=280, height=50, bg="purple")
        self.status_panel.grid(row=2,column=0,padx=10,pady=10)

        self.status_label = tk.Label(self.status_panel,text="Status")
        self.status_label.grid(row=0,column=0,padx=5,pady=5)

        # abilities+equipment
        self.abilityequipment_panel = tk.Frame(self.right_panel, width=280, height=300, bg="purple")
        self.abilityequipment_panel.grid(row=3,column=0,padx=10,pady=10)

        # Abilities
        self.ability_panel = tk.Frame(self.abilityequipment_panel, width=120, height=300, bg="yellow")
        self.ability_panel.grid(row=0,column=0,padx=10,pady=10)

        # Equipment
        self.equipment_panel = tk.Frame(self.abilityequipment_panel, width=120, height=300, bg="yellow")
        self.equipment_panel.grid(row=0,column=1,padx=10,pady=10)

class FrameWorld(BaseFrame):
    """Shows worldgen map"""
    def createWidgets(self):
        world = self.frameController.controller.worlds[0]
        self.map = widgets.MapRenderer(self,world,(0,0))
        self.map.grid(row=0,column=1)

        self.main_menu_button = tk.Button(self,text="Switch to main view",command=lambda: self.frameController.showFrame(FrameHome))
        self.main_menu_button.grid(row=0,column=0)
        return