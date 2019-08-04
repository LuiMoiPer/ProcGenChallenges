class AlchemyCircle:

    def __init__(self, center, radius, sides, order=1, rotation=0):
        #need
        pass

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, coord):
        self._center = coord
        #update points
        pass

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
        #set the new order
        #update degenerate
        #update lines
            #update intersections
            #update inlineRadius
        pass

    @property
    def points(self):
        return self._points

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        #update points
        pass

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation
        #update points
            #update segmentLines
            #update lines
                #update intersections
        pass

    @property
    def segmentLines(self):
        return self._segmentLines

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, sides):
        #update order
        #update points
            #update segmentLines
            #update lines
                #update intersections
                #update inlineRadius
        pass

    #Updaters
    def _updateInlineRadius(self):
        #uses center
        #uses lines
        pass

    def _updateIntersections(self):
        #uses lines
        #uses order
        pass

    def _updateLines(self):
        #uses order
        #uses points
        _updateIntersections()
        _updateInlineRadius()
        pass

    def _updatePoints(self):
        #uses rotation
        #uses sides
        _updateLines()
        _updateSegmentLines()
        pass

    def _updateSegmentLines(self):
        #uses center
        #uses points
        pass

    @classmethod
    def random(cls):
        pass

    @staticmethod
    def getAngle(point1, point2):
        pass

    @staticmethod
    def getDistance(point1, point2):
        pass

    @staticmethod
    def getIntersection(line1, line2):
        pass

    @staticmethod
    def getMidpoint(point1, point2):
        pass

    #doesn't handle whether things are opaque or not
    @staticmethod
    def getSvg():
        pass
