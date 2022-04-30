import math


class Plane:
    def __init__(self, initialState, id, loc):
        self.x, self.y = loc
        self.heading = self.getHeadingToCenter()
        self.id = id
        self.current_state = initialState
        self.current_state.run()

    def __str__(self): return self.action

    @property
    def name(self):
        return ''

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    def getHeadingToCenter(self):
        degrees = math.atan2(self.y, self.x);


    def getPosition(self):
        return self.x, self.y

    def getHeading(self):
        return self.heading