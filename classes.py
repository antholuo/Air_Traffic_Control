# SpaceRyde Internship Coding Challenge
# classes.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math
import pygame
import random

from consts import *  # there should be nothing BUT global constants here

"""Some notes to myself:
- 10hz = 10 times per second
- 1km = 1000m
- planes spawn on edges
- arbitrary number of planes
- planes travel to base of runway in straight lines.
    - turns / changes angle instantaneously to follow path of runway. speed is same throughout.
- runways equidistant from center
- queue airplanes based on time of arrival.
- multithread for data simplicity, nothing we need is heavy enough to need multiprocessing.

- headings are only integers.

=========================================================
Some assumptions I made:
- Center of circle is center of the world (0,0) in x,y
- for our purposes, and in the name of time, we can assume that longitude and lattitude are basically x,y coordinates
    - (no need to worry about translating them?)
- Nothing is mentioned about the ATC being able to talk back to the planes, it seems as if the planes spawn, and then
move directly towards the center of the circle?
    - > there are no commands from atc to the planes to move in any way.... all we have ar the following:
        > STOP (holding pattern)
        > RUNWAY (which runway to go to).
    ->> alternatively, we can only give straight lines for planes to fly to.
"""

"""Code components (brainstorming):
- map trajectories -> ensure no collisions.
- queues planes
- randomly spawns planes.

Instructions:
[[heading, location], [heading, location]]
Fly each heading until you reach a location.
"""

"""
todo:
^ compute number of holding positions available (easy grid problem while maintaining at least one access on each side
- have atc generate paths
    - to cells, find nearest inner cell, navigate towards using A*. <- every cell will have some access ring that can be got to.
    - for landing, generate hop from empty cell to empty cell using A*, then generate straight line to runway end
- check flight paths inside main while loop.

- visualization? <- probably won't happen
"""


class Plane():
    def __init__(self, id, degrees):
        self.id = id
        self.x = math.cos(degrees)
        self.y = math.sin(degrees)
        self.heading = 180 + (90 - degrees)  # global heading.
        self.state = 0

        """States for the plane:
        0: entering our airspace
        1: guided towards holding location
        2: holding
        3: guided towards landing target
        4: landed/landing"""

    def update_heading(self, heading):
        self.heading = heading

    def update_location(self):
        self.x = self.x + math.sin(self.heading) * AIRSPEED
        self.y = self.y + math.cos(self.heading) * AIRSPEED

    def get_location(self):
        return self.x, self.y

    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def set_holding(self):
        self.state = 2

    def set_to_hold(self):
        self.state = 1

    def set_to_land(self):
        self.state = 3

    def set_landed(self):
        self.state = 4


class HoldingLoc():
    def __init__(self, x, y, parkable=True, radius=HOLD_RADIUS, vacant=True, ):
        self.x = x
        self.y = y
        self.loc = x, y  # not sure if I will need this but might be nice to have in case
        self.vacant = True
        self.radius = HOLD_RADIUS
        self.occupant = None
        self.is_parkable = parkable

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_full(self, plane_id):
        self.vacant = False
        self.occupant = plane_id

    def is_vacant(self):
        return self.vacant

    def set_vacant(self):
        self.vacant = True
        self.occupant = None


class Runway():
    def __init__(self, center, length=RUNWAY_LENGTH, width=RUNWAY_WIDTH):
        """

        :param center: (x,y) of the center of the runway
        :param length:
        :param width:
        """
        self.North_Target = center[1] + RUNWAY_LENGTH / 2
        self.South_Target = center[1] - RUNWAY_LENGTH / 2
        self.in_use = False

    def set_in_use(self):
        self.in_use = True

    def get_status(self):
        if self.in_use:
            return "occupied"  # occupied
        else:
            return "vacant"

    def get_centerline(self):
        return self.center[0]

    def get_southtarget(self):
        return self.South_Target

    def get_northtarget(self):
        return self.North_Target