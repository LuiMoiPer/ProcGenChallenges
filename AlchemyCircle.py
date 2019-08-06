from math import acos, cos, degrees, hypot, radians, sin, sqrt

class AlchemyCircle:

    def __init__(self, center, radius, sides, order=1, rotation=0):
        ## TODO: error checking
        self._center = center
        self._radius = radius
        self._sides = sides
        self._order = order
        self._rotation = rotation
        self._updatePoints()
        self._updateDegenerate()
        pass

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, coord):
        ## TODO: error checking
        self._center = coord
        self._updatePoints()

    @property
    def degenerate(self):
        return self._degenerate

    @property
    def inlineRadius(self):
        return self._inlineRadius

    ## TODO: add intersetion with segmentLines
    @property
    def intersections(self):
        return self._intersections

    @property
    def lines(self):
        return self._lines

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        ## TODO: error checking
        self._order = order
        self._updateDegenerate()
        self._updateLines()

    @property
    def points(self):
        return self._points

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        ## TODO: error checking
        self._radius = radius
        self._updatePoints()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        ## TODO: error checking
        self._rotation = rotation
        self._updatePoints()

    @property
    def segmentLines(self):
        return self._segmentLines

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, sides):
        ## TODO: error checking
        self._sides = sides
        self._order = 1
        self._updatePoints()

    #Updaters
    def _updateDegenerate(self):
        if self.order == 1:
            self._degenerate = False
        elif self.sides % self.order == 0:
            self._degenerate = True
        else:
            self._degenerate = False

    def _updateInlineRadius(self):
        midpoint = AlchemyCircle.getMidpoint(self.points[0], self.points[1])
        self._inlineRadius = AlchemyCircle.getDistance(self.center, midpoint)

    def _updateIntersections(self):
        if self.order == 1:
            self._intersections = []
        else:
            self._intersections = []
            for currLine in range(self.sides):
                for crosLine in range(currLine - self.order + 1, currLine):
                    # TODO: fix index out of range, sides = 6 order = 2
                    intersection = AlchemyCircle.getIntersection(self.lines[currLine], self.lines[crosLine])
                    self._intersections.append(intersection)

    def _updateLines(self):
        if self.order == 1:
            self._lines = []
            for i in range(len(self.points)):
                line = (self.points[i], self.points[(i + 1) % len(self.points)])
                self._lines.append(line)
        else:
            self._lines = []
            currLine = 0
            for i in range(self.sides):
                line = (self.points[currLine], self.points[(currLine + self.order) % self.sides])
        self._updateIntersections()
        self._updateInlineRadius()

    def _updatePoints(self):
        self._points = []
        bounds = self.getOutlineBounds()
        step = 360.0 / self.sides
        for deg in [i * step + self.rotation for i in range(self.sides)]:
            #make coord on unit circle then shift it so (0, 0) is top left
            point = (cos(radians(deg)) + 1, sin(radians(deg)) + 1)
            #scale and offset the coord so they fit the bounding box
            point = (point[0] * self.radius, point[1] * self.radius)
            point = (point[0] + bounds[0][0], point[1] + bounds[0][1])
            self._points.append(point)
        self._updateLines()
        self._updateSegmentLines()

    def _updateSegmentLines(self):
        self._segmentLines = []
        for point in self.points:
            self._segmentLines.append((point, self.center))

    def getInlineBounds(self):
        upperLeftBound = (self.center[0] - self.inlineRadius, self.center[1] - self.inlineRadius)
        lowerRightBound = (self.center[0] + self.inlineRadius, self.center[1] + self.inlineRadius)
        return (upperLeftBound, lowerRightBound)

    def getOutlineBounds(self):
        upperLeftBound = (self.center[0] - self.radius, self.center[1] - self.radius)
        lowerRightBound = (self.center[0] + self.radius, self.center[1] + self.radius)
        return (upperLeftBound, lowerRightBound)

    # TODO:
    #doesn't handle whether things are opaque or not
    def getSvg():
        pass

    # TODO:
    @classmethod
    def random(cls):
        pass

    @staticmethod
    def getAngle(origin, point):
        vector1 = (point[0] - origin[0], point[1] - origin[1])
        magVector1 = hypot(vector1[0], vector1[1])
        angle = acos(vector1[0]/magVector1)
        angle = degrees(angle)
        if vector1[1] < 0:
            angle = 360 - angle
        return angle

    @staticmethod
    def getDistance(point1, point2):
        return hypot((point1[0] - point2[0]), (point1[1] - point2[1]))

    @staticmethod
    def getIntersection(line1, line2):
        x = 0
        y = 1

        p0 = line1[0]
        p1 = line1[1]
        p2 = line2[0]
        p3 = line2[1]

        a1 = p1[y] - p0[y]
        b1 = p0[x] - p1[x]
        c1 = a1 * p0[x] + b1 * p0[y]

        a2 = p3[y] - p2[y]
        b2 = p2[x] - p3[x]
        c2 = a2 * p2[x] + b2 * p2[y]

        denominator = a1 * b2 - a2 * b1
        if denominator == 0:
            return None
        x = (b2 * c1 - b1 * c2) / denominator
        y = (a1 * c2 - a2 * c1) / denominator
        return (x,y)

    @staticmethod
    def getMidpoint(point1, point2):
        return ((point1[0]+point2[0])/2, (point1[1]+point2[1])/2)
