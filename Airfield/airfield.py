# defines our entire airfield

class Runway:
    def __init__(self, center_x, center_y, width, length):
        self.x = center_x
        self.y = center_y
        self.width = width
        self.length = length
        self.x_edges = (center_x - width/2, center_x + width/2)
        self.y_edges = (center_y - length/2, center_y + length/2)

class Airfield:
    def __init__(self, radius, num_runways=2, runway_length=1000, runway_width=500, runway_spacing = 500):
        self.num_runways = num_runways # load this from configuration file later
        self.radius = radius
        self.runway_length = runway_length
        self.runway_width = runway_width
        self.runways = self.generate_runways()

    def generate_runways(self):
        # generates runways and returns some data
        runways = []
        for i in range(0, self.num_runways):
            runways.append(i)
        return runways