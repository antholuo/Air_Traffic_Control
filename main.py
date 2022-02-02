# SpaceRyde Internship Coding Challenge
# main.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math
import pygame

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

"""

"""
todo:
- compute number of holding positions available (easy grid problem while maintaining at least one access on each side
- have atc generate paths to/from holding cells.
- visualization?
"""


class Plane():
    def __init__(self, id, degrees):
        self.id = id
        self.x = math.cos(degrees)
        self.y = math.sin(degrees)
        self.heading = 180 + (90 - degrees)  # global heading.
        self.state = 0;
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
    def __init__(self, x, y, vacant=True, radius=HOLD_RADIUS):
        self.x = x
        self.y = y
        self.loc = x, y  # not sure if I will need this but might be nice to have in case
        self.vacant = True
        self.radius = HOLD_RADIUS
        self.occupant = None

    def set_full(self, plane_id):
        self.vacant = False
        self.occupant = plane_id

    def set_vacant(self):
        self.vacant = True
        self.occupant = None


class Controller():
    # everything talks to the controller, and the controller has complete control over everything (theoretically)
    def __init__(self, radius, planes=[], runway_width=RUNWAY_WIDTH, runway_length=RUNWAY_LENGTH,
                 num_runways=NUM_RUNWAYS, holding_locs=[]):
        self.radius = radius
        self.planes = planes  # in case there are existing planes which need to be handled
        self.runway_width = runway_width
        self.runway_length = runway_length
        self.num_runways = num_runways
        self.holding_locs = holding_locs
        self.num_spots = len(holding_locs) - 1

    def add_plane(self, plane, id):
        if self.num_spots > 0:
            self.planes.append(plane)
        else:
            plane.update_heading(plane.heading + 180)  # turn around the plane

    def hold_plane(self, plane, spot):
        # plane is already in position to hold
        # assume that if they are within the area of a holding pattern, they can self navigate to spin in circles
        plane_loc = plane.get_location()
        plane.set_holding()
        spot.set_full(plane.get_id)


def main():
    return


if __name__ == "__main__":
    main()
