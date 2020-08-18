'''

physics.py

Author: Jordan Hay
Date: 2020-07-24

A 2D physics simulation in Python 3

'''

# -- Imports --

import math # Mathematical functions etc
from time import time # Used to get the time since the epoch
from time import sleep # Pause program for a length of time
from copy import copy

# -- Objects --

# Vectors for vector maths
class Vector:

    ''' 
    Vector()

    Vectors for vector maths.
    '''

    def __init__(self):

        # Initialise empty polar form vector
        self._magnitude = 0
        self._argument = 0

    # Generate vector from x and y magnitudes
    def from_xy(self, x, y):

        '''
        from_xy(x, y)

        Generates the vector object from x and y magnitudes

        x (float) - Magnitude on x-axis
        y (float) - Magnitude on y-axis
        '''

        # Set input to object vars after xy to polar conversion
        self._magnitude, self._argument = xy_to_polar(x, y)

        return(self) # Return self so that vector object can be initialised using this command

    # Generate vector from polar description
    def from_polar(self, magnitude, argument):

        '''
        from_polar(magnitude, argument)

        Generates the vector object from a magnitude and an argument

        magnitude (float) - The magnitude/length of the vector
        argument (float) - Angle measured from right horizontal in degrees
        '''

        # Set the input to object vars
        self._magnitude = magnitude
        self._argument = argument

        return(self) # Return self so that vector object can be initialised using this command

    # Convert polar form to x,y form and return
    def return_xy(self):
        '''
        return_xy()

        Returns the x and y magnitudes of the vector
        '''

        x = 0 # Store x magnitude to return
        y = 0 # Store y magnitude to return

        # Calculate the magnitudes of our x and y vectors using trigonometric functions
        x = self._magnitude * math.cos(math.radians(self._argument))
        y = self._magnitude * math.sin(math.radians(self._argument))

        return(x, y) # Return the calculated x and y values

    def return_polar(self):

        '''
        return_polar()

        Returns the magnitude and argument of the vector
        '''

        return(self._magnitude, self._argument) # Return the object variables

    def magnitude(self):

        return(self._magnitude)

    def argument(self):

        return(self._argument)

    # Add another vector object to our vector object
    def add(self, add_vectors):

        '''
        add(add_vectors)

        Vector addition. Adds vectors in list to current vector

        add_vectors (list) - A list of vectors to be added to the current vector
        '''

        # Get the x and y values of original vector
        x, y = self.return_xy()
        
        # Check there are add vectors first
        if(add_vectors is not None):
        # For every vector to be added
            for add_vector in add_vectors:

                x += add_vector.return_xy()[0] # Add the x components  
                y += add_vector.return_xy()[1] # Add the y components

            # Assign converted to polar values to own
            self._magnitude, self._argument = xy_to_polar(x, y)

        return(self) # Return self so that vector object can be initialised using this command

# The physics environment that an object or objects exist in
class PhysicsEnvironment:

    def __init__(self, acceleration_vectors = [], name = None):

        self._acceleration_vectors = copy(acceleration_vectors)
        self._time = 0
        self._objects = [] # list of physics objects that are present in the environment
        self._name = name # Optional name for easier sorting

    def get_acceleration_vectors(self):

        return(copy(self._acceleration_vectors))

    def get_time(self):

        return(self._time)

    def add_object(self, new_object):

        self._objects.append(new_object)

    def increment_time(self, increment):

        self._time += increment

    def simulate(self, runtime, increment, realtime = False):

        total_runtime = 0

        while(total_runtime < runtime):

            for obj in self._objects:

                obj.update_time()

                print(f"{obj.name()}\n(x, y): {obj.global_position()}, \n(magnitude, argument): {obj.velocity().return_polar()}\n--")

            self.increment_time(increment)

            total_runtime += increment

            # If we're trying to simulate in real time then sleep for the increment time
            if(realtime): 
                sleep(increment)

class PhysicsObject:

    '''
    PhysicsObject()

    Describes objects to be simulated under the laws of physics

    mass (float) - The mass of the object in kilograms
    init_velocity (Vector object) - A Vector object describing the initial velocity of the object
    init_position (list [x, y]) - Coordinates of the objects initial position
    acceleration_vectors (list of Vector objects) - A list of Vector objects that act as acceleration on the object
    init_time (float) - The time in the physics simulation when the object was initiated
    '''

    # Initialisation
    def __init__(self, environment, mass = 0, init_velocity = Vector().from_polar(0, 0), init_position = [0, 0], acceleration_vectors = [], init_time = 0, name = None):

        self._environment = environment # The environment in which the object exists
        self._mass = mass # Mass of our object
        self._init_velocity = init_velocity # Velocity of the object at initialisation
        self._init_position = init_position # The initial position of the object
        self._acceleration_vectors = acceleration_vectors + self._environment.get_acceleration_vectors() # Vectors that are accelerating our object
        self._init_time = init_time # The time at which the physics object was created
        self._time = 0 # Adjusted time of the object
        self._name = name # Optional name variable to allow object tracking easier in some cases

        self._environment.add_object(self) # Add self to list of objects in the physics environment

    # Update object adjusted time using global physics time and own init time
    def update_time(self):

        self._time = self._environment.get_time() - self._init_time # Return time adjusted with vector init_time

    def name(self):

        return(self._name)

    def environment(self):

        return(self._environment)

    def mass(self):

        return(self._mass)

    def new_init(self, new_velocity, new_time, new_position):

        self._init_velocity = new_velocity
        self._init_time = new_time
        self._init_position = new_position

    # Calculate the acceleration acting on the object as a vector
    def acceleration(self):

        return(Vector().from_polar(0, 0).add(self._acceleration_vectors)) # Add the acceleration vectors to a blank vector and return it

    # Calculte the momentum of the object as a vector
    def momentum(self):

        return(Vector().from_polar(self.velocity().return_polar()[0] * self._mass, self.velocity().return_polar()[1])) # Create a vector from velocity magnitude * mass of the object for the magnitde and the argument of the velocity

    # Calculate the current direction and magnitude of velocity at the time
    def velocity(self):

        init_vel_x, init_vel_y = self._init_velocity.return_xy() # Get initial velocity x and y components

        accel_x, accel_y = self.acceleration().return_xy() # get acceleration x and y components

        vel_x, vel_y = (velocity_equation(init_vel_x, accel_x, self._time), velocity_equation(init_vel_y, accel_y, self._time)) # Calculate the x and y components of the final velocity in time

        magnitude, argument = xy_to_polar(vel_x, vel_y) # Convert into polar form

        return(Vector().from_polar(magnitude, argument)) # Create and return a vector from polar form

    # Calculate the x, y position of the object (relative to start point)
    def relative_position(self):

        init_vel_x, init_vel_y = self._init_velocity.return_xy() # Get x and y components of initial velocity

        accel_x, accel_y = self.acceleration().return_xy() # Get x and y components of acceleration vectors

        x = distance_equation(init_vel_x, self._time, accel_x) # Calculate x position
        y = distance_equation(init_vel_y, self._time, accel_y) # Calculate y position

        return(x, y) # Return as x and y coordinates

    # Calculate position of the object in the global environemnt
    def global_position(self):

        x, y = self.relative_position() # Calculate the relative position

        x += self._init_position[0] # Add on x init position
        y += self._init_position[1] # Add on y init position

        return(x, y) # Return global position

    # Collide two objects together
    def collide(self, col_object):

        mass_dif = self.mass() - col_object.mass()
        total_mass = self.mass() + col_object.mass()

        vel_x, vel_y = self.velocity().return_xy()
        obj_x, obj_y = col_object.velocity().return_xy()

        x_sep = self.global_position()[0] - col_object.global_position()[0]
        y_sep = self.global_position()[1] - col_object.global_position()[1]

        sep_angle = math.degrees(math.atan(y_sep/x_sep))

        vel_x = ((vel_x * math.degrees(math.cos(self.momentum().argument() - sep_angle)) * total_mass + (2 * col_object.mass() * obj_x * math.degrees(math.cos(col_object.momentum().argument() - sep_angle)))) / total_mass) * math.degrees(math.cos(sep_angle)) + math.degrees(math.sin(self.momentum().argument() - sep_angle)) * math.degrees(math.cos(sep_angle + math.pi/2))
        vel_y = ((vel_x * math.degrees(math.cos(self.momentum().argument() - sep_angle)) * total_mass + (2 * col_object.mass() * obj_x * math.degrees(math.cos(col_object.momentum().argument() - sep_angle)))) / total_mass) * math.degrees(math.sin(sep_angle)) + math.degrees(math.sin(self.momentum().argument() - sep_angle)) * math.degrees(math.cos(sep_angle + math.pi/2))

        self.new_init(Vector().from_xy(vel_x, vel_y), self.environment().get_time(), self.global_position())

# -- Functions --

# Calculates the kinematic equation for distance
def distance_equation(init_vel, time, accel):

    distance = (init_vel * time) + (0.5 * accel * (time ** 2)) # Calculate distance travelled using kinematic equation

    return(distance) # Return calculated distance

# Calculates the kinematic equation for final velocity
def velocity_equation(init_vel, accel, time):

    vel = init_vel + (accel * time) # Calculate velocity in time using kinematic equation

    return(vel) # Return calculated velocity

# Convert x and y magnitudes to polar values
def xy_to_polar(x, y):

    magnitude = 0 # Store magnitude to return
    argument = 0 # Store argument to return

    # Get the magnitude of the resultant vector using pythagorean theorom
    magnitude = math.sqrt((x ** 2) + (y ** 2))

    argument = math.degrees(math.asin(y/magnitude)) # Use trig to calculate the argument

    return(magnitude, argument) # Return magnitude and argument

# -- Constants --

EARTH_GRAVITY = Vector().from_polar(9.8, -90)

# -- Main --

# If this is the main module then start a simulation that we can use for testing the engine
if(__name__ == "__main__"):

    environment = PhysicsEnvironment(acceleration_vectors = [EARTH_GRAVITY])

    PhysicsObject(environment, 1, Vector().from_polar(100, 45), [0, 0], name = "Object1")

    environment.simulate(10, 1)
