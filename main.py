# SpaceRyde Internship Coding Challenge
# classes.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math
import pygame
import random
import numpy as np

from consts import *  # there should be nothing BUT global constants here
from classes import *
from utils import *
from visualization import *

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


class Controller():
    # everything talks to the controller, and the controller has complete control over everything (theoretically)
    def __init__(self, radius, runway_width=RUNWAY_WIDTH, runway_length=RUNWAY_LENGTH,
                 num_runways=NUM_RUNWAYS, holding_locs=[]):
        self.radius = radius
        self.planes = []  # in case there are existing planes which need to be handled
        self.runways = []
        self.runway_width = runway_width
        self.runway_length = runway_length
        self.num_runways = num_runways
        self.holding_locs, self.lanes = holding_locs  # tuples of places that you can be in
        self.empty_locs = holding_locs[0]
        self.occupied_locs = {}

    def add_runway(self, runway):
        # choose to add here because runways could be different daily
        self.runways.append(runway)

    def rm_runway(self, runway):
        self.runways.remove(runway)  # thankfully python remove lets us remove by value

    def add_plane(self, plane, id):
        if len(self.empty_locs) > 0:
            plane_instruction_pair = plane, [],  # consists of the plane, and future queued instructions.
            self.planes.append(plane_instruction_pair)  # this makes it easier to assign instructions later
        else:
            plane.update_heading(plane.heading + 180)  # turn around the plane

    def get_planes(self):
        return self.planes

    def get_first_plane(self):
        return self.planes[0][0], self.planes[0][0].get_id()

    def try_holding(self, plane, idx, spot):
        self.planes[idx] = plane, instructions_to_spot(plane, spot, self.lanes)


    def hold_plane(self, plane, spot):
        # plane is already in position to hold
        # assume that if they are within the area of a holding pattern, they can self navigate to spin in circles
        plane_loc = plane.get_location()
        plane.set_holding()

    def try_landing(self, plane, idx):

        for runway in self.runways:
            # todo: add a system to determine closest points from runways, and then check in that priority
            if runway.get_status == "vacant":  # no priority for one runway over another.
                self.planes[idx] = plane, instructions_to_land(plane, runway)
                plane.set_to_land()
        else:
            plane.set_holding()  # continue holding

        # compute heading

    def run(self):
        id = 0
        while (True):
            # main control loop
            if (np.random.rand() > 0.7):
                # if we're unlucky, we get a new plane in our airspace.
                newplane = generate_plane(id)
                self.add_plane(newplane, id)
                self.try_holding(newplane, id, find_nearest_spot(self.holding_locs, id))
                id += 1

            if (check_flight_paths(self.get_planes()) < 4) and len(self.get_planes()) > 0:
                plane, id = self.get_first_plane()
                self.try_landing(plane, id)  # land the next plane in the queue
        return "Day over good job!"


def setup() -> Controller:
    # starts up our controller

    horiz = RUNWAY_WIDTH / 2 + RUNWAY_SPACING / 2
    center = horiz, 0
    runway1 = Runway(center)
    center = -horiz, 0
    runway2 = Runway(center)

    Tower = Controller(ATC_RADIUS, holding_locs=generate_spots())
    Tower.add_runway(runway1)
    Tower.add_runway(runway2)
    return Tower


def check_flight_paths(planes):
    """
    Checks to make sure that planes are still on the right flight path.
    Note that planes is a list, and within each list there are three elements:
        plane, curr heading, instructions.
    :param planes:
    :return:
    """
    in_flight = 0
    for flier in planes:
        if flier[0].get_state() == 4:
            planes.remove(flier)  # remove any landed planes
        if flier[0].get_state() == 3:  # in flight
            if (equals(flier[0].get_location(), flier[1][0][1])):
                flier[1].pop()  # removes first/current instruction from the list.
                if (flier[1][0][0]):  # if there is a new instruction
                    flier[0].update_heading(flier[1][0][0])  # sets new heading
                else:
                    flier[0].set_landed()  # no more instructions, we have landed?
            in_flight += 1
        if flier[0].get_state() == 1:  # to hold
            if (equals(flier[0].get_location(), flier[1][0][1])):
                flier[1].pop()  # removes first/current instruction from the list.
                if (flier[1][0][0]):  # if there is a new instruction
                    flier[0].update_heading(flier[1][0][0])  # sets new heading
                else:
                    flier[0].set_holding()  # no more instructions, we have reached holding cell?
            in_flight += 1

    return in_flight


def main():
    # run setup (creating ATC, finding spots, etc)
    Tower = setup()
    Tower.run()

if __name__ == "__main__":
    main()
