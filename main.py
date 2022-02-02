# SpaceRyde Internship Coding Challenge
# main.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math
import pygame

from consts import * # there should be nothing BUT global constants here

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
        self.holding = False
        self.heading = 180 + (90 - degrees)  # global heading.

    def update_heading(self, heading):
        self.heading = heading

    def update_location(self):
        self.x = self.x + math.sin(self.heading) * AIRSPEED
        self.y = self.y + math.cos(self.heading) * AIRSPEED

    def set_holding(self, holding = True): # typed in case we forget to set holding.
        self.holding = holding;

class Controller():
    def __init__(self, radius, planes = {}, runway_width = RUNWAY_WIDTH, runway_length = RUNWAY_LENGTH, num_runways = NUM_RUNWAYS):
        self.radius = radius
        self.planes = planes # in case there are existing planes which need to be handled
        self.runway_width = runway_width
        self.runway_length = runway_length
        self.num_runways = num_runways

    def add_plane(self, plane, id):
        self.planes[id] = plane

def main():
    return


if __name__ == "__main__":
    main()
