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

        super(GUIEnvironment, self).__init__(acceleration_vectors, name) # Run through parent init command

        # Initialise canvas object
        self._canvas = tk.Canvas(parent, width = self._width, height = self._height)
        self._canvas.place(x = 0, y = 0)

# An object in the environment
class GUIObject(phy.PhysicsObject):

    # Initialisation
    def __init__(self, environment, physics = False, mass = 0, init_velocity = phy.Vector().from_polar(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0, name = None):

        self._environment = environment
        self._physics = physics

        # If physics is enabled
        if(self._physics):

            # Run through parent init command
            super(GUIObject, self).__init__(environment, mass = 0, init_velocity = phy.Vector().from_polar(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0, name = None)

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
    e = GUIEnvironment(root, [phy.EARTH_GRAVITY], root.winfo_screenwidth(), root.winfo_screenheight(), "Room 1")

    # Exit button
    exit_btn = ttk.Button(root, text = "Close", command = root.destroy)
    exit_btn.place(x = 10, y = 10)

    # -- Mainloop --
    root.mainloop()
