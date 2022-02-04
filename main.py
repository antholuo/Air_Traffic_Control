# SpaceRyde Internship Coding Challenge
# main.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math
import pygame
import random

from consts import *  # there should be nothing BUT global constants here
from utils import generate_spots, instructions_to_spot, instructions_to_land, equals, generate_plane

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
    def __init__(self, x, y, parkable=True, radius=HOLD_RADIUS, vacant=True,):
        self.x = x
        self.y = y
        self.loc = x, y  # not sure if I will need this but might be nice to have in case
        self.vacant = True
        self.radius = HOLD_RADIUS
        self.occupant = None
        self.is_parkable = parkable

    def set_full(self, plane_id):
        self.vacant = False
        self.occupant = plane_id

    def set_vacant(self):
        self.vacant = True
        self.occupant = None


class Runway():
    def __init__(self, center, length=RUNWAY_LENGTH, width=RUNWAY_WIDTH):
        self.North_Target = center + RUNWAY_LENGTH / 2
        self.South_Target = center - RUNWAY_LENGTH / 2
        self.in_use = False

    def set_in_use(self):
        self.in_use = True

    def get_status(self):
        if self.in_use:
            return "occupied"  # occupied
        else:
            return "vacant"

class Controller():
    # everything talks to the controller, and the controller has complete control over everything (theoretically)
    def __init__(self, radius, planes=[], runway_width=RUNWAY_WIDTH, runway_length=RUNWAY_LENGTH,
                 num_runways=NUM_RUNWAYS, holding_locs=[]):
        self.radius = radius
        self.planes = planes  # in case there are existing planes which need to be handled
        self.runways = []
        self.runway_width = runway_width
        self.runway_length = runway_length
        self.num_runways = num_runways
        self.holding_locs = holding_locs # tuples of places that you can be in
        self.empty_locs = holding_locs
        self.occupied_locs = {}

    def add_runway(self, runway):
        # choose to add here because runways could be different daily
        self.runways.append(runway)

    def rm_runway(self, runway):
        self.runways.remove(runway)  # thankfully python remove lets us remove by value

    def add_plane(self, plane, id):
        if self.num_spots > 0:
            plane_instruction_pair = plane, []  # consists of the plane, and future queued instructions.
            self.planes.append(plane_instruction_pair)  # this makes it easier to assign instructions later
        else:
            plane.update_heading(plane.heading + 180)  # turn around the plane

    def get_planes(self):
        return self.planes

    def try_holding(self, plane, idx, spot):
        self.planes[idx] = plane, instructions_to_spot(plane, spot)

    def hold_plane(self, plane, spot):
        # plane is already in position to hold
        # assume that if they are within the area of a holding pattern, they can self navigate to spin in circles
        plane_loc = plane.get_location()
        plane.set_holding()
        spot.set_full(plane.get_id)  # sets this spot to be full!
        self.occupied_locs[plane.get_id] = spot  # set this spot to be matched with plane id
        self.empty_locs.remove(spot)

    def try_landing(self, plane, idx):
        spot = self.occupied_locs[plane.get_id]
        self.occupied_locs.pop(plane.get_id)
        self.empty_locs.append(spot)
        spot.set_vacant

        for runway in self.runways:
            # todo: add a system to determine closest points from runways, and then check in that priority
            if runway.get_status == "vacant":  # no priority for one runway over another.
                self.planes[idx] = plane, instructions_to_land(plane, runway)
                plane.set_to_land()
        else:
            plane.set_holding()  # continue holding

        # compute heading


def setup() -> Controller:
    return

def check_flight_paths(planes: list[Plane]):
    """
    Checks to make sure that planes are still on the right flight path.
    Note that planes is a list, and within each list there are three elements:
        plane, curr heading, instructions.
    :param planes:
    :return:
    """
    return

def main():
    # run setup (creating ATC, finding spots, etc)
    Tower = setup()
    id = 0
    while(True):
        # main control loop
        if(random() > 0.7):
            # if we're unlucky, we get a new plane in our airspace.
            Tower.add_plane(generate_plane(), id)
            id += 1
        check_flight_paths()


    return


if __name__ == "__main__":
    main()
