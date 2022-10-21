import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Tk Example")
    root.minsize(200, 200)  # width, height
    root.maxsize(1280, 720)  # width, height
    root.geometry("1280x720+50+50")
    root.config(bg="skyblue")

    main_panel = tk.Frame(root,width=900, height=700)
    main_panel.grid(row=0,column=0,padx=10,pady=10)

    log_panel = tk.Frame(main_panel,width=900, height=550, bg="purple")
    log_panel.grid(row=0,column=0,padx=10,pady=10)

    activity_panel = tk.Frame(main_panel,width=900, height=100, bg="purple")
    activity_panel.grid(row=1,column=0,padx=10,pady=10)

    right_panel = tk.Frame(root,width=340, height=700)
    right_panel.grid(row=0,column=1,padx=10,pady=10)

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
    status_label.grid(row=0,column=0,padx=10,pady=10)

    # abilities+equipment
    abilityequipment_panel = tk.Frame(right_panel, width=280, height=350, bg="purple")
    abilityequipment_panel.grid(row=3,column=0,padx=10,pady=10)

    # Abilities
    ability_panel = tk.Frame(abilityequipment_panel, width=120, height=350, bg="yellow")
    ability_panel.grid(row=0,column=0,padx=10,pady=10)

    # Equipment
    equipment_panel = tk.Frame(abilityequipment_panel, width=120, height=350, bg="yellow")
    equipment_panel.grid(row=0,column=1,padx=10,pady=10)

    root.mainloop()




if __name__ == "__main__":
    main()