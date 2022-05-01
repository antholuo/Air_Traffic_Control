from plane import Plane
from plane import State
from Utils.ATC_CONSTS import *
import math


# i really have no clue how to make a state machine

class Flying(State):
    def updateHeading(self, heading: float) -> None:
        self.plane.heading = heading

    def updatePosition(self, delta_seconds: float = 0.1) -> (float, float, float):
        # calculate how far we have flown in delta time.
        # also updates the planes position

        # returns updated position in a straight line.
        lat = math.radians(self.plane.lat)
        lon = math.radians(self.plane.lon)
        dist = PLANE_AIRSPEED * delta_seconds

        heading = self.plane.heading

        newlat = math.asin(
            math.sin(lat) * math.cos(dist / EARTH_RADIUS) + math.cos(lat) * math.sin(dist / EARTH_RADIUS) * math.cos(
                heading))
        newlon = lon + math.atan2(math.sin(heading) * math.sin(dist / EARTH_RADIUS) * math.cos(lat),
                                  math.cos(dist / EARTH_RADIUS) - math.sin(lat) * math.sin(newlat))
        heading = self.plane.heading

        newlat = math.degrees(newlat)
        newlon = math.degrees(newlon)

        self.plane.lat = newlat
        self.plane.lon = newlon

        return newlat, newlon, heading


class Holding(State):
    def updateHeading(self, heading: float) -> None:
        self.plane.heading = heading
        self.plane.setState(Flying())

    def updatePosition(self, delta_seconds: float = 0.1) -> (float, float, float):  # hope default val is ok
        # update position after circling around.

        # first calculate how far it is possible to fly, then turn that into arclength
        # calculate triangle with original position, arclength.
        # get new heading
        # get new position
        newlat = 0
        newlon = 0
        heading = self.plane.heading
        return newlat, newlon, heading
