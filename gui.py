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
from time import time

# -- Classes --
    
# The environment that an object or objects exist in
class GUIEnvironment(phy.PhysicsEnvironment):

    # Initialisation command
    def __init__(self, parent, acceleration_vectors = [], height = 100, width = 100, name = None):

        self._parent = parent # Parent GUI element
        self._width = width # Width of canvas
        self._height = height # Height of canvas
        self._shape_to_object = {}

        super(GUIEnvironment, self).__init__(acceleration_vectors, name) # Run through parent init command

        # Initialise canvas object
        self._canvas = tk.Canvas(parent, width = self._width, height = self._height)
        self._canvas.place(x = 0, y = 0)

    # Return the canvas object
    def canvas(self):

        return(self._canvas)

    # Simulate the environment, overwrites the physics simulation with a graphical interpretation
    def simulate(self):

        self.increment_time(0.1) # Increment time

        # For every object in the environment
        for obj in self._objects:

            # Update time
            obj.update_time()

            # Move the object
            obj.move()

            # Collision detection
            x1, y1, x2, y2 = self._canvas.coords(obj.shape())

            for col_shp in self._canvas.find_overlapping(x1, y1, x2, y2):

                if(obj.shape() != col_shp):

                    col_obj = self._objects[col_shp - 1]
                    
                    obj.collide(col_obj)
                    col_obj.collide(obj)
                    obj.reset_xy()
                    col_obj.reset_xy()

        # Schedule next simulation point
        self._parent.after(10, self.simulate)
            
# An object in the environment
class GUIObject(phy.PhysicsObject):

    # Initialisation
    def __init__(self, environment, shape, physics = False, mass = 0, init_velocity = phy.Vector().from_polar(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0, name = None):

        self._environment = environment # Graphical and physical environment the object exists in
        self._physics = physics # Flag for whether the object is physics enabled or not
        self._x = 0
        self._y = 0

        # Generating the object shape
        if(shape["shape"] == "rectangle"):

            self._shape = self._environment.canvas().create_rectangle(init_position[0], init_position[1], init_position[0] + shape["width"], init_position[1] + shape["height"], fill = shape["fill"])

        # If physics is enabled
        if(self._physics):

            # Run through parent init command
            super(GUIObject, self).__init__(environment, mass, init_velocity, init_position, acceleration_vectors, init_time, name)

    def shape(self):

        return(self._shape)

    def reset_xy(self):

        self._x = 0
        self._y = 0

    # Move object
    def move(self):

        x, y = self.relative_position() # get position relative to start position
        
        # Modify to be only magnitudes of change
        x -= self._x 
        y -= self._y

        # Add change to recorded change
        self._x += x
        self._y += y

        print(f"Moved X: {x}, Y: {-y}")

        # Move the objects as per movement magnitudes
        # -y is because magnitudes are used opposite to how I would use them
        self._environment.canvas().move(self._shape, x, -y)

# -- Variables --

root = tk.Tk()

# -- Main --

if(__name__ == "__main__"):

    # -- tk setup --
    root.title("Physics Simulation")
    root.geometry("500x500+50+50")

    # Environment
    e = GUIEnvironment(root, [phy.EARTH_GRAVITY], 500, 500, "Room 1")
    
    # Exit button
    exit_btn = ttk.Button(root, text = "Close", command = root.destroy)
    exit_btn.place(x = 10, y = 10)

    # Start button
    start_btn = ttk.Button(root, text = "Start", command = e.simulate) # Command starts simulation
    start_btn.place(x = 10, y = 40)

    # Test physics enabled object
    GUIObject(e, {"shape": "rectangle", "width": 10, "height": 10, "fill": "black"}, True, 1, phy.Vector().from_polar(30, 70), [100, 100], name = "Test")

    GUIObject(e, {"shape": "rectangle", "width": 10, "height": 10, "fill": "black"}, True, 1, phy.Vector().from_polar(30, 120), [200, 100], name = "Test")

    root.mainloop() # GUI event loop