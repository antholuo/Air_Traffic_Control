# SpaceRyde Internship Coding Challenge
# utils.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

import math

from classes import HoldingLoc, Plane
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
    lanes = []
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
                            lanes.append(spot) # this should not be needed in the end, but is an optimization that we make
                    double = 0;
                else:
                    for i in range(-1, 0):
                        for j in range(-1, 0):
                            spot = HoldingLoc(i * x, j * y, parkable=True, vacant=True)
                            spots.append(spot)
                    double += 1;

            theta += 10  # not sure how many degrees is good

        generative_radius += RADIUS_STEP

    return spots, lanes  # by nature of spots, the closest spots are first in the list.

def find_respective_runway(x, y):
    """
    Finds the nearest runway opening quadrant wise. Hardcoded since I'm running out of time.
    Finds quadrant and maps to respective runway in that quadrant.
    Could be made to pythagoras and identify nearest runway and factor in things like approach heading, etc.
    :param x:
    :param y:
    :return: tuple of x,y locations to fly to
    """
    RUNWAY_LT = -RUNWAY_SPACING/2 - RUNWAY_WIDTH/2, RUNWAY_LENGTH/2
    RUNWAY_LB = -RUNWAY_SPACING/2 - RUNWAY_WIDTH/2, -RUNWAY_LENGTH/2
    RUNWAY_RT =  RUNWAY_SPACING/2 + RUNWAY_WIDTH/2, RUNWAY_LENGTH/2
    RUNWAY_RB =  RUNWAY_SPACING/2 + RUNWAY_WIDTH/2, -RUNWAY_LENGTH/2

    if x>=0 and y>=0:
        return RUNWAY_RT
    elif x>=0 and y<=0:
        return RUNWAY_RB
    elif x<=0 and y<=0:
        return RUNWAY_LB
    elif x<=0 and y>=0:
        return RUNWAY_RT
    else:
        # some sort of emergency I guess? To be dealt with later.
        return 0,0

def instructions_to_land(plane, runway, lanes):
    # find nearest runway opening
    # find nearest lane node to heading.
    # set final destination reasonable distance (90 degrees from landing heading) intersecting with final lane node.
    # use a special search that computes how close we are to the centerline instead of an absolute.
    targ_loc = 0,0
    if pythagoras(runway.get_centerline(), runway.get_northtarget(), plane.get_location[0], plane.get_location[1]) < pythagoras(runway.get_centerline(), runway.get_southtarget(), plane.get_location[0], plane.get_location[1]):
        targ_loc = runway.get_centerline(), runway.get_northtarget + 3000 # adding some distance so that the system is not messed up
    else:
        targ_loc = runway.get_centerline(), runway.get_southtarget - 3000

    current_loc = plane.get_location()

    return search(current_loc, targ_loc, lanes)


def instructions_to_spot(plane, spot, lanes):
    """
    Wrapper for search() function (makes it easier to call in our code).
    :param plane:
    :param spot:
    :param lanes:
    :return:
    """
    current_loc = plane.get_location()
    targ_loc = spot.get_x, spot.get_y
    return search(current_loc, targ_loc, lanes)

def find_nearest_lane_node(lanes: list[HoldingLoc], current_loc = (0,0), destination = None) -> HoldingLoc:
    """
    Finds the nearest node designated to be used for air traffic movement
    :param lanes:
    :param current_loc:
    :param destination:
    :return:
    """
    if destination == None:
        # just looking for the nearest lane node to begin with
            # -> can be optimized further to  find lane node in specific direction.
        nearest = lanes[0]
        dist = 22000  # unreasonably large number to start with
        for spot in lanes:
            temp_dist = pythagoras(current_loc[0], current_loc[1], spot.get_x, spot.get_y)
            if temp_dist < dist:
                dist = temp_dist
                nearest = spot
    else:
        # find spot closest to the end point.
        nearest = lanes[0]
        dist = 22000  # large distance to start with
        for spot in lanes:
            temp_dist = pythagoras(current_loc[0], current_loc[1], spot.get_x, spot.get_y)
            dist_to_dest = pythagoras(destination[0], destination[1], spot.get_x, spot.get_y)
            if temp_dist < 5000 and dist_to_dest < dist:
                dist = temp_dist
                nearest = spot
        # centers of two adjacent lane nodes should not be more than 5000km away -> but there is no way for there to be multiple in this range

    return nearest

def compute_heading(x1, y1, x2, y2) -> int:
    # computes the heading that you need to fly to get from x1, y1 to x2, y2
    # we know x1, y1, x2, y2. This gives all sides of the triangle? tan = opp/adj, = x2-x1 / y2-y1

    degs = math.atan((x2-x1), (y2-y1)) / (math.pi * 180)
    if degs < 0:
        degs += 360
    return math.round(degs)


def search(current_loc, targ_loc, lanes: list[HoldingLoc], landing = False)->list[[int, tuple]]:
    """
    Search algorithm to find headings to go towards specified final target location.
    :param current_loc: current plane x,y location
    :param targ_loc:    target plane x,y location
    :param cells:       list of holdinglocations that we can treat as nodes
    :return: instruction data type, with pairs of headings and distances.
    """
    """
    There are a few ways to do this:
        - we can try to find the shortest line from our current location to our target location, and then move points around such that we
        do not intersect with any occupied nodes
        - find the closest open node in an assigned traffic lane and then follow until our target location
            - in this case, most nodes should be in one of the 4 quadrants, and thus will be assigned to one of the 4 ends of the runways, with
            each quadrant corresponding to one of the quadrants. This means that traffic should never cross over each other.
            - each destination is in one quadrant. Search towards that direction
        - some combination of both where we try to see if there are "shortcuts" that can be made after generating our traffic lane path
        - we can also map everything as a graph....
        """
    # find nearest open node (there should only be 1 within a certain radius of....HOLD_RADIUS+TRAFFIC_MIN_DIST + BUFFER
    path = []
    cell = find_nearest_lane_node(lanes, current_loc, targ_loc) # start with our first cell
    path.append(compute_heading(current_loc[0], current_loc[1], cell.get_x, cell.get_y), cell.get_x, cell.get_y)
    while( ((pythagoras(cell.get_x, cell.get_y, targ_loc[0], targ_loc[1]) > 2200) and landing==False) or ((math.abs(cell.get_x - targ_loc[0]) > 2200) and landing==True)):
        # while we are not yet at the final approach landing state
        next = find_nearest_lane_node(lanes, cell.get_x, cell.get_y, targ_loc[0], targ_loc[1])
        path.append(compute_heading(cell.get_x, cell.get_y, next.get_x, next.get_y), next.get_x, next.get_y)
        cell = next # there should be no issue with this. See test1 in test.py

    if landing:
        # add final path to landing.
        # cell should still be our final cell.
        # we maintain our cell_y, but move x target to the centerline of the runway
        path.append(compute_heading(cell.get_x, cell.get_y, targ_loc[0], cell.get_y), targ_loc[0], cell.get_y)
        path.append(compute_heading(targ_loc[0], cell.get_y, targ_loc[0], 0), 0, 0) # final landing path to center of runway

    return path