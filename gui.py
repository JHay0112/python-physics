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

    # Initialisation command
    def __init__(self, parent, acceleration_vectors = [], height = 100, width = 100, name = None):

        self._parent = parent # Parent GUI element
        self._width = width # Width of canvas
        self._height = height # Height of canvas

        super(Environment, self).__init__(acceleration_vectors, name) # Run through parent init command

        # Initialise canvas object
        self._canvas = tk.Canvas(parent, width = self._width, height = self._height)
        self._canvas.place(x = 0, y = 0)

# -- Functions --

# -- Constants --

# -- Variables --

root = tk.Tk() # Root GUI instance

# -- Main --

if(__name__ == "__main__"):

    # -- tk setup --
    root.title("Physics Simulation")
    root.attributes("-fullscreen", True)

    # Environent
    e = Environment(root, [phy.EARTH_GRAVITY], root.winfo_screenwidth(), root.winfo_screenheight(), "Room 1")

    # Exit button
    exit_btn = ttk.Button(root, text = "Close", command = root.destroy)
    exit_btn.place(x = 10, y = 10)

    # -- Mainloop --
    root.mainloop()
