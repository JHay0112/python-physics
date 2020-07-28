'''

physics.py

Author: Jordan Hay
Date: 2020-07-24

'''

# -- Imports --

import math # Mathematical functions etc
from time import time # Used to get the time since the epoch
from time import sleep # Pause program for a length of time
import copy # For copying lists

# -- Objects --

# Vectors for vector maths
class Vector:

    # Initialise empty polar form vector
    magnitude = 0
    argument = 0

    # Generate vector from x and y magnitudes
    def from_xy(self, x, y):

        # Set input to object vars after xy to polar conversion
        self.magnitude, self.argument = xy_to_polar(x, y)

    # Generate vector from polar description
    def from_polar(self, magnitude, argument):

        # Set the input to object vars
        self.magnitude = magnitude
        self.argument = argument

    # Convert polar form to x,y form and return
    def return_xy(self):

        x = 0 # Store x magnitude to return
        y = 0 # Store y magnitude to return

        # Calculate the magnitudes of our x and y vectors using trigonometric functions
        x = magnitude * math.cos(argument)
        y = magnitude * math.sin(argument)

        return(x, y)

    # Add another vector object to our vector object
    def add(self, add_vectors):

        # Get the x and y values of original vector
        x, y = self.return_xy()

        for add_vector in add_vectors:

            x += add_vector.return_xy()[0]
            y += add_vector.return_xy()[1]

        # Assign converted to polar values to own
        self.argument, self.magnitude = xy_to_polar(x, y)

class PhysicsObject:

    # Initialisation
    def __init__(self, mass = 0, init_velocity = Vector(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0):

        global physics_objects

        self.mass = mass # Mass of our object
        self.init_velocity = init_velocity # Velocity of the object at initialisation
        self.init_position = init_position
        self.acceleration_vectors = acceleration_vectors
        self.init_time = init_time
        self.time = 0

        physics_objects.extend(self) # Add self to list of physics_objects

    # Update object adjusted time using global physics time and own init time
    def update_time(self):

        global physics_time # Get physics time global

        return(physics_time - self.init_time) # Return time adjusted with vector init_time

    # Calculate the acceleration acting on the object as a vector
    def acceleration(self):

        return(Vector(0, 0).add(self.acceleration_vectors))

    # Calculte the momentum of the object as a vector
    def momentum(self):

        return(Vector(self.direction().magnitude * self.mass, self.direction().argument))

    # Calculate the current direction and magnitude of velocity at the time
    def velocity(self):

        update_time()

        init_vel_x, init_vel_y = self.init_velocity.return_xy()

        accel_x, accel_y = acceleration().return_xy()

        vel_x, vel_y = (velocity_equation(init_vel_x, accel_x, time), velocity_equation(init_vel_y, accel_y, self.time))

        magnitude, argument = xy_to_polar(vel_x, vel_y)

        return(Vector(magnitude, argument))

    def position(self):

        init_vel_x, init_vel_y = self.init_velocity.return_xy()

        accel_x, accel_y = acceleration().return_xy()

        x = distance_equation(init_vel_x, self.time, accel_x)
        y = distance_equation(init_vel_y, self.time, accel_y)

        return([x, y])

# -- Functions --

# Calculates the kinematic equation for distance
def distance_equation(init_vel, time, accel):

    distance = (init_vel * time) + (0.5 * accel * (time ** 2))

    return(distance)

# Calculates the kinematic equation for final velocity
def velocity_equation(init_vel, accel, time):

    vel = init_vel + (accel * time)

    return(vel)

# Convert x and y magnitudes to polar values
def xy_to_polar(x, y):

    magnitude = 0 # Store magnitude to return
    argument = 0 # Store argument to return

    # Get the magnitude of the resultant vector using pythagorean theorom
    magnitude = math.sqrt((x ** 2) + (y ** 2))

    # Check that y is not zero else an error will be produced if we try and run trigonometric function
    if(y == 0):
        # if the y is zero then the argument is zero
        argument = 0
    else:
        # Else calculate argument using trigonemtric equation
        argument = math.atan(x/y)

    return(argument, magnitude)

# -- Variables --

physics_objects = [] # List of all physics objects
physics_time = 0 # Record what "time" it is in the system 

# -- Main --
