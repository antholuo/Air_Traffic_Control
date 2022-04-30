# ATC Tower class
import math
import sys


class Tower:
    def __init__(self, airfield):
        self.tower_id = 0;
        self.airfield = airfield;

    def land_plane(self, plane):
        #handles the last vectors for the plane.
        # finds nearest landing strip endpoint
        dist = sys.maxsize
        x,y = 0,0 #targets to fly to
        for runway in self.airfield.runways:
            dist1 = (plane.x - runway.x) **2  + (plane.y - runway.y_edges[0]) **2

            dist2 = (plane.x - runway.x) **2 + (plane.y - runway.y_edges[1]) **2
            if dist2<dist1:
                dist = dist2
                x, y = runway.x, runway.y_edges[1]
            else:
                dist = dist1
                x, y = runway.x, runway.y_edges[0]
        self.gen_landing_path(plane, (x,y))
        return

    def gen_landing_path(self, plane, loc):
        # futur: make it so that this will draw a nice spline.
        # for now, this creates a heading for the plane to fly.
        x,y = loc
        heading = math.atan((plane.x-x), (plane.y-y))
        plane.give_instruction(heading)