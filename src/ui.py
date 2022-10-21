import tkinter as tk

class GUI:
    """Container for the game gui"""
    def __init__(
        self
    ):
        self.root = tk.Tk()
        self.root.title("Tk Example")
        self.root.minsize(200, 200)  # width, height
        self.root.maxsize(1280, 720)  # width, height
        self.root.geometry("1280x720+50+50")
        self.root.config(bg="skyblue")

        self.top_bar = tk.Frame(self.root,width=1260,height=30)
        self.top_bar.grid(row=0,column=0,padx=5,pady=5)

        self.quit_button = tk.Button(self.top_bar,text="Quit", command=self.root.quit)
        self.quit_button.pack(side="right")

        self.title_label = tk.Label(self.top_bar,text="Title")
        self.title_label.pack(side="left")

        self.bottom_panel = tk.Frame(self.root)
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
        return

    def guiStart(
        self
    ):
        self.root.mainloop()