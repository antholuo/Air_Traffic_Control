from plane import Plane
from plane import State

# i really have no clue how to make a state machine

class Flying(State):
    def updateHeading(self, heading: float) -> None:
        self.plane.heading = heading

    def updatePosition(self, delta_seconds: float=1):
        # calculate how far we have flown in delta time.
        x = 0
        y = 0
        heading = self.plane.heading
        return x, y, heading

class Holding(State):
    def updateHeading(self, heading: float) -> None:
        self.plane.heading = heading
        self.plane.setState(Flying())

    def updatePosition(self, delta_seconds: float=1) -> (float, float, float):
        x = 0
        y = 0
        heading = self.plane.heading
        return x, y, heading