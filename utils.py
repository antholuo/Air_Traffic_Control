# SpaceRyde Internship Coding Challenge
# utils.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math

from main import HoldingLoc, Plane
from consts import *

"""utils.py
Contains utilities such as: calculating collisions, determining number of parking spots, etc"""


def pythagoras(x1, y1, x2, y2):
    return math.round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))  # just to return nearest int of pythagoras distance


def equals(a, b) -> bool:
    # quick function to check if two things are equal within an arbitrary constant.
    # Should use function overrides.
    if math.abs(a - b) <= 50:
        return True
    return False


def generate_plane() -> Plane:
    # randomly generates a plane
    return


def generate_spots() -> list[HoldingLoc]:
    # exclude the center airfield, as well as the extended centerlines of the runways.
    # generate left side and then generate right side.
    runway_center = (math.floor((NUM_RUNWAYS - 1) / 2)) * RUNWAY_WIDTH + (
            NUM_RUNWAYS - 1) * RUNWAY_SPACING + RUNWAY_WIDTH / 2
    generative_radius = HOLD_RADIUS + RUNWAY_SPACING / 2 + RUNWAY_WIDTH + TRAFFIC_MIN_DIST
    RADIUS_STEP = HOLD_RADIUS + TRAFFIC_MIN_DIST
    spots = []
    double = 0
    while generative_radius < (ATC_RADIUS-2000): #subtract 2000 since we need to leave access ring on the outside
        # leaving the runway widths open.
        # for each radius width, we add to one quadrant, and then reflect it to generate the 4 mirrored quadrants
        # make sure that the x-distance from the centerline of the runways is at least 1.5km
        x = generative_radius
        y = 0
        theta = 0
        while (x - runway_center) > 1500:  # from what I remember, this should re-evaluate every time
            # as long as there is 1500m distance between holding center and runway center
            oldx, oldy = x, y
            x = math.cos(theta)
            y = math.sin(theta)
            if (pythagoras(oldx, oldy, x, y) >= 2200):
                # there is more than 2200 meters between planes
                if double == 1:
                    # second spot in a row, leave a lane for planes to fly to
                    for i in range(-1, 0):
                        for j in range(-1, 0):
                            # i and j will go through all combinations of x,y combinations
                            spot = HoldingLoc(i * x, j * y, parkable=False, vacant=True)
                            spots.append(spot)
                    double = 0;
                else:
                    for i in range(-1, 0):
                        for j in range(-1, 0):
                            spot = HoldingLoc(i * x, j * y, parkable=True, vacant=True)
                            spots.append(spot)
                    double += 1;

            theta += 10  # not sure how many degrees is good

        generative_radius += RADIUS_STEP

    return spots  # by nature of spots, the closest spots are first in the list.


def instructions_to_land(plane, runway):
    # find nearest runway opening
    # navigate heading to line up with runway.
    # once on runway heading, land plane.
    return


def instructions_to_spot(plane, spot):
    # instead of trying to find the paths that the plane fits through (since it has a minimum gflying distance),
    # take radius of all objects and increase that and then run A*.
    return

def astar(current_loc: tuple(float, float), targ_loc)->list[[int, tuple(float, float)]]:
    """

    :param current_loc: current plane x,y location
    :param targ_loc:    target plane x,y location
    :return: instruction data type, with pairs of headings and distances.
    """
    