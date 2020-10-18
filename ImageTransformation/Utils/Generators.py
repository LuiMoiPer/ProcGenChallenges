from DataStructures import Point2d
class Delta:
    def __init__(self):
        self._points = set()

    def __len__(self):
        len(self._points)

    @property
    def points(self):
        return list(self._points)

    def add(self, point):
        self._points.add(point)
        
    def update(self, points):
        self._points.update(points)
    
    def remove(self, point):
        self._points.discard(point)

    def shift(self, delta):
        for point in self._points:
            point += delta

    def scale(self, scalar):
        for point in self._points:
            point *= scalar

    @staticmethod
    def cardinal():
        return [Point2d(-1, 0),
            Point2d(1, 0),
            Point2d(0, -1),
            Point2d(0, 1)
        ]
    
    @staticmethod
    def ordinal():
        return [Point2d(-1, -1),
            Point2d(-1, 1),
            Point2d(1, -1),
            Point2d(1, 1)
        ]

    @staticmethod
    def octinal():
        return Delta.cardinal + Delta.ordinal

    @staticmethod
    def knight():
        return [Point2d(-2, -1),
            Point2d(-2, 1),
            Point2d(2, -1),
            Point2d(2, 1),
            Point2d(-1, -2),
            Point2d(1, -2),
            Point2d(-1, 2),
            Point2d(1, 2)
        ]

    @staticmethod
    def circle(radius):
        points = []
        for x in range(radius):
            for y in range(radius):
                point = Point2d(x, y)
                if point.distance_from_origin <= radius:
                    points.append(point)
                    points.append(Point2d(x, -y))
                    points.append(Point2d(-x, y))
                    points.append(Point2d(-x, -y))
        return points

if __name__ == "__main__":
    d = Delta()
    d.add(Point2d(1,2))
    d.update([Point2d(x,x) for x in range(3)])
    ""