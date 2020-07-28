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
    def add_vectors(self, add_vectors):

        # Get the x and y values of original vector
        x, y = self.return_xy()

        for add_vector in add_vectors:

            x, y += add_vector.return_xy()
        
        # Assign converted to polar values to own
        self.argument, self.magnitude = xy_to_polar(x, y)

'''
# Stores an object that has physics applied to it
class PhysicsObject:

    # Initialisaion
    # name (str) - The name of the object, to make it easier to identify which object we are getting the name of
    # environment (obj) - The PhysicsEnvironment that the physics object is apart of
    # mass (int) - Mass in kgs of the objects
    # velocity (obj) - Vector describing the initial velocity of the physics object
    # position (dict) - Cartesian coordinates of the object
    # forces (list) - List of vector forces applied to the object
    # init_time (int) - Time in seconds at which the velocity vector applies to
    def __init__(self, name, environment, mass, velocity, position, forces = [], init_time = None):

        # Assign parameters to object attributes
        self.name = name
        self.environment = environment
        self.mass = mass
        self.init_velocity = velocity
        self.velocity = velocity
        self.position = position
        self.start_position = copy.copy(position) # Using copy to ensure changes do not link
        self.forces = forces
        self.forces.extend(self.environment.forces) # Add physics environement forces to item
        self.init_time = init_time # In a sense this is the absolute time
        self.time = 0 # Making this time relative to the vector

        self.environment.objects.append(self) # Append this object to list of physics object in the environement

        # If init time has not been set make it that same as the current phys time
        if(self.init_time is None):
            self.init_time = self.environment.phys_time

        self.set_time(self.init_time) # Set time to be init_time

    # Adjust time relative with the init time and then set as relative time
    def set_time(self, time):

        self.time = time - self.init_time # Set time adjusted relative to init_time 

    # Print out information relevant to self
    def info(self):

        print(f"Name: {self.name}, Mass: {self.mass}kg, Velocity: {self.velocity.magnitude}m/s, momentum: {self.momentum().magnitude}kgm/s, X: {self.position[0]}m Y: {self.position[1]}m, X Velocity: {self.velocity.return_xy()[0].magnitude}m/s, Y Velocity: {self.velocity.return_xy()[1].magnitude}m/s")

    # Caculate and return object momentum vector
    def momentum(self):

        return(Vector(self.mass * self.direction_vector().magnitude, self.direction_vector().argument))

    # Calculate the resultant vector
    def resultant_vector(self):

        result = self.init_velocity # Set vector to be velocity

        result.add(self.forces_vector()) # add forces vector to velocity vector

        return(result)

    # Calculate the vector of applied forces
    def forces_vector(self):

        result = Vector(0, 0) # Create blank vector

        # For every force applied to object
        for force in range(0, len(self.forces)):

            result.add(self.forces[force]) # Add force vector to result vector

        return(result)

    # Vector that returns vector at point in time
    def direction_vector(self):

        # Get the initial velocity
        init_vel_x = self.init_velocity.return_xy()[0].magnitude
        init_vel_y = self.init_velocity.return_xy()[1].magnitude

        # Get accelerations
        accel_x = self.forces_vector().return_xy()[0].magnitude
        accel_y = self.forces_vector().return_xy()[1].magnitude

        # Calculate x and y vectors for current velocity
        vel_x = velocity_equation(init_vel_x, accel_x, self.time)
        vel_y = velocity_equation(init_vel_y, accel_y, self.time)

        result = Vector(0, 0) # Blank vector
        result.add(Vector(vel_x, 0)) # Add the x vector
        result.add(Vector(vel_y, 90)) # Add the y vector

        return(result)

    # Update the vector information
    def update(self):

        # Get x and y velocity
        vel_x, vel_y = self.init_velocity.return_xy()

        # Set to be magnitudes
        vel_x = vel_x.magnitude
        vel_y = vel_y.magnitude 

        # Get x and y acceleration magnitude
        accel_x = self.forces_vector().return_xy()[0].magnitude
        accel_y = self.forces_vector().return_xy()[1].magnitude
        
        # Set the current velocity to be the direction vector
        self.velocity = self.direction_vector()

        # Set the updated position
        self.position[0] = distance_equation(vel_x, self.time, accel_x) + self.start_position[0]
        self.position[1] = distance_equation(vel_y, self.time, accel_y) + self.start_position[1]

    # Collide our object with another
    def collide(self, collision_object):

        print(f"Collision between {self.name} and {collision_object.name}")

        # Add our total momentum together on each axis
        x_total_momentum = self.momentum().return_xy()[0]
        x_total_momentum.add(collision_object.momentum().return_xy()[0])
        y_total_momentum = self.momentum().return_xy()[1]
        y_total_momentum.add(collision_object.momentum().return_xy()[1])

        # Total mass
        total_mass = self.mass + collision_object.mass

        # Divide the magnitudes by the mass
        x_velocity = x_total_momentum.magnitude / total_mass
        y_velocity = y_total_momentum.magnitude / total_mass

        # Add the vectors together
        result = Vector(0, 0)
        result.add(Vector(x_velocity, 0))
        result.add(Vector(y_velocity, 90))

        # Set the new initial velocities and times
        self.init_velocity = result
        self.init_time = self.time

        collision_object.init_velocity = result
        collision_object.init_time = collision_object.time
'''

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

# -- Main --


