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

    # Return the canvas object
    def canvas(self):

        return(self._canvas)

    # Simulate the environment, overwrites the physics simulation with a graphical interpretation
    def simulate(self, runtime, increment):

        pass

# An object in the environment
class GUIObject(phy.PhysicsObject):

    # Initialisation
    def __init__(self, environment, shape, physics = False, mass = 0, init_velocity = phy.Vector().from_polar(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0, name = None):

        self._environment = environment # Graphical and physical environment the object exists in
        self._shape = shape # Holds shape of the object
        self._physics = physics # Flag for whether the object is physics enabled or not

        # If physics is enabled
        if(self._physics):

            # Run through parent init command
            super(GUIObject, self).__init__(environment, mass = 0, init_velocity = phy.Vector().from_polar(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0, name = None)

# -- Variables --

root = tk.Tk() # Root GUI instance

# -- Main --

if(__name__ == "__main__"):

    # -- tk setup --
    root.title("Physics Simulation")
    root.attributes("-fullscreen", True)

    # Environment
    e = GUIEnvironment(root, [phy.EARTH_GRAVITY], root.winfo_screenwidth(), root.winfo_screenheight(), "Room 1")

    # Exit button
    exit_btn = ttk.Button(root, text = "Close", command = root.destroy)
    exit_btn.place(x = 10, y = 10)

    # Test physics enabled object
    o = GUIObject(e, e.canvas().create_rectangle(50, 50, 60, 60, fill = "black"), True, 1, name = "Test")

    # Begin physics simulation
    e.simulate(10, 1)

    # -- Mainloop --
    root.mainloop()
