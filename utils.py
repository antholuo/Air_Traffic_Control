# SpaceRyde Internship Coding Challenge
# utils.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math

from consts import *

"""utils.py
Contains utilities such as: calculating collisions, determining number of parking spots, etc"""

def generate_spots():
    # exclude the center airfield, as well as the extended centerlines of the runways.
    # generate left side and then generate right side.
    generative_radius = HOLD_RADIUS + RUNWAY_SPACING / 2 + RUNWAY_WIDTH + TRAFFIC_MIN_DIST
    double = 0
    RADIUS_STEP = HOLD_RADIUS + TRAFFIC_MIN_DIST
    while generative_radius < ATC_RADIUS:
        if double == 1:
            double = 0
            generative_radius += RADIUS_STEP
        # create spots starting from left and right side, leaving space at ends for runway access (this makes sense).

    return

def instructions_to_land(plane, runway):
    return

def instructions_to_spot(plane, spot):
    return