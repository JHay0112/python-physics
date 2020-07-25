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

    # Init
    # magnitude (int) - The magnitude of the vector
    # argument (int) - The angle of the vector from horizontal
    def __init__(self, magnitude, argument):

        # Assign paramaters to the object attributes
        self.magnitude = magnitude
        self.argument = argument

    # Print out information about the vector
    def info(self):

        print(f"Magnitude: {self.magnitude}, Argument: {self.argument}")

    # Return the x and y sub-vectors as a tuple
    def return_xy(self):

        argument = math.radians(self.argument) # Make a copy of our argument in radians for math.sin and math.cos

        # Calculate the magnitudes of the x and y vectors (using SOHCAHTOA) and create new vector objects
        x = Vector(self.magnitude * math.cos(argument), 0)
        y = Vector(self.magnitude * math.sin(argument), 90)

        return(x, y) # return x, y as a tuple

    # Add another vector to our vector
    def add(self, add_vector):

        self_x, self_y = self.return_xy() # Get x and y vectors from our vector
        add_x, add_y = add_vector.return_xy() # Get x and y vectors from vector to be added

        x = self_x.magnitude + add_x.magnitude # Add x magnitudes
        y = self_y.magnitude + add_y.magnitude # Add y magnitudes

        # Calculate magnitude for new vector using pythag thereom
        magnitude = math.sqrt((x ** 2) + (y ** 2))

        # Calculate argument using x and y vectors using SOHCAHTOA
        argument = math.degrees(math.asin(y/magnitude))

        # Update our magnitdue and argument with the new ones
        self.magnitude = magnitude
        self.argument = argument

# The environment in which all the physics objects are held
class PhysicsEnvironment:

    gravity = Vector(-10, 90) # Gravity vector, same as earth's
    forces = [gravity] # List of force vectors
    objects = [] # Store objects inside environement
    phys_time = 0 # Store how long the physics simulation has been running

    # Run physics simulation
    # increment (int) - incrememnt in seconds for running the simulation
    def simulate(self, increment):

        run_simulation = True # Flag for the loop

        while(run_simulation):

            run_start = time() # Get time for when running started

            # For every object in our environment
            for o in self.objects:
                
                o.set_time(self.phys_time) # set the object time to be the same as simulation time
                o.update() # Update our object
                self.check_for_collisions()
                o.info() # Display info of the object

            self.phys_time += increment # Increment the environments by the set increment

            run_end = time() # Get time for when running ended

            runtime = run_end - run_start # Calculate how long the set of code took to run

            sleep(increment - runtime) # Sleep for the increment time minus how long the previous code took to run

    # Check for collisions between objects
    def check_for_collisions(self):

        pass

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

# -- Functions --

# Calculates the kinematic equation for distance
def distance_equation(init_vel, time, accel):

    distance = (init_vel * time) + (0.5 * accel * (time ** 2))

    return(distance)

# Calculates the kinematic equation for final velocity
def velocity_equation(init_vel, accel, time):

    vel = init_vel + (accel * time)

    return(vel)

# -- Variables --

wind_vector = Vector(7, 180) # Example additional force vector
environment = PhysicsEnvironment() # Initialise the physics environment

# -- Main --

PhysicsObject("Ball", environment, 1, Vector(50, 45), [0, 0]) # Create a new physics object

environment.simulate(1) # Begin simulation with updates every 1 second