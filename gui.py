'''

gui.py

Author: Jordan Hay
Date: 2020-08-11

Graphics for physics engine

'''

# -- Imports --

import physics as phy # The physics engine
import tkinter as tk # GUI
from tkinter import ttk # More GUI

# -- Classes --

# The environment that an object or objects exist in
class GUIEnvironment(phy.PhysicsEnvironment):

    pass

# -- Functions --

# -- Constants --

# -- Variables --

root = tk.Tk() # Root GUI instance

# -- Main --

if(__name__ == "__main__"):

    # -- tk setup --
    root.title("Physics Simulation")
    root.attributes("-fullscreen", True)

    # Exit button
    exit_btn = ttk.Button(root, text = "Close", command = root.destroy)
    exit_btn.place(x = 10, y = 10)

    # -- Mainloop --
    root.mainloop()
