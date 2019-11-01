#!/usr/bin/python3

class Point:
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    def __repr__(self):
        return f'<Point: x{self.x}, y{self.y}>'

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x,y)

    def __iadd__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def __isub__(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

    def __itruediv__(self, other):
        self.x = self.x / float(other)
        self.y = self.y / float(other)
        return self

    def __itruediv__(self, other):
        self.x = self.x * float(other)
        self.y = self.y * float(other)
        return self

    def __mul__(self, other):
        x = self.x * float(other)
        y = self.y * float(other)
        return Point(x,y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x,y)

    def __truediv__(self, other):
        x = self.x / float(other)
        y = self.y / float(other)
        return Point(x,y)


    def asTuple(self):
        return (self.x, self.y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @staticmethod
    def getDistance(point1, point2):
        return hypot((point1[0] - point2[0]), (point1[1] - point2[1]))

class Polygon:
    def __init__(self, points):
        self._verticies = points
        self._calcCentroid()

    @property
    def center(self):
        return self._center

    @property
    def centroid(self):
        return self._centroid

    @property
    def sides(self):
        return self._sides

    @property
    def verticies(self):
        return self._verticies

    @property
    def verticiesAsTuples(self):
        vertsAsTuples = []
        for point in self._verticies:
            vertsAsTuples.append(point.asTuple())
        return vertsAsTuples

    def _calcCentroid(self):
        totalArea = 0
        currPoint = None
        nextPoint = None
        centroid = Point(0,0)

        for i in range(len(self._verticies) - 1):
            currPoint = self._verticies[i]
            nextPoint = self._verticies[i + 1]
            area = currPoint.x * nextPoint.y - nextPoint.x * currPoint.y
            totalArea += area
            centroid.x += (currPoint.x + nextPoint.x) * area
            centroid.y += (currPoint.y + nextPoint.y) * area

        currPoint = self._verticies[-1]
        nextPoint = self._verticies[0]
        area = currPoint.x * nextPoint.y - nextPoint.x * currPoint.y
        totalArea += area
        centroid.x += (currPoint.x + nextPoint.x) * area
        centroid.y += (currPoint.y + nextPoint.y) * area

        totalArea *= 0.5;
        centroid.x /= (6.0 * totalArea)
        centroid.y /= (6.0 * totalArea)

        self._centroid = centroid
