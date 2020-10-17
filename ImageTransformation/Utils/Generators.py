from DataStructures import Point2d
class Delta:
    def __init__(self):
        self._points = set()

    def __len__(self):
        len(self._points)

    def add(self, point):
        self._points.add(point)
        
    def update(self, points):
        self._points.update(points)

    


if __name__ == "__main__":
    d = Delta()
    d.add(Point2d(1,2))
    d.update([Point2d(x,x) for x in range(3)])
    ""