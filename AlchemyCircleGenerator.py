#make a couple concentric circles
from PIL import Image, ImageDraw
from math import cos, sin, radians, sqrt
def main():
    #make Image
    img = Image.new('RGB', (1000, 1000), 'hsb(5,0%,50%)')
    draw = ImageDraw.Draw(img)

    bounds = [(100, 100), (900, 900)]
    lines = getStarLines(bounds, sides=8, rotation=22, order=3)
    drawLines(draw, lines)
    drawOutline(draw, getPolygon(bounds, sides=8, rotation=22))
    img.show()

# TODO: replace
def drawLayer(draw, bounds, sides=3, offset=0, outerCircle=True, innerCircle=True, centerLines=False, fill=None):
    polygon = getPolygon(bounds, sides, offset)
    if outerCircle:
        draw.ellipse(bounds)
    draw.polygon(polygon['coords'], outline='hsb(5,0%,100%)',fill=fill)
    if centerLines:
        for line in polygon['lines']:
            draw.line(line)
    if innerCircle:
        draw.ellipse(polygon['innerCircleBounds'])
    return polygon


def getPolygon(bounds, sides=3, rotation=0):
    if sides < 2:
        sides = 2
    polygonInfo = {
        'outlineBounds': bounds,
        'center': getMidpoint(bounds[0], bounds[1]),
        'sides': sides,
        'rotation': rotation
    }
    #use bounds to set sizes
    size = getDistance(polygonInfo['center'], getMidpoint(bounds[0], (bounds[0][0], bounds[1][1])))
    #make the coords for each point of the polygon
    points = []
    for deg in range(0+rotation, 360+rotation, round(360/sides)):
        #make coord on unit circle then shift it so (0, 0) is top left
        point = (cos(radians(deg))+1, sin(radians(deg))+1)
        #scale and offset the coord so they fit the bounding box
        point = (point[0]*size, point[1]*size)
        point = (point[0]+bounds[0][0], point[1]+bounds[0][1])
        points.append(point)
    #used to remove extra coords that sometimes occurs due to rounding
    if len(points) > sides:
        del points[-1]
    polygonInfo['points'] = points
    #find and set the bounds for the circle that touches each side at its midpoint
    if sides > 2:
        center = polygonInfo['center']
        midpoint = getMidpoint(points[0], points[1])
        radius = getDistance(center, midpoint)
        inscribeBounds = [(center[0]-radius, center[1]-radius), (center[0]+radius, center[1]+radius)]
        polygonInfo['inscribeBounds'] = inscribeBounds
    else:
        polygonInfo['inscribeBounds'] = bounds
    return polygonInfo

def getPolygonLines(shapeInfo):
    lines = []
    for i in range(len(shapeInfo['points'])):
        line = [shapeInfo['points'][i], shapeInfo['points'][(i+1)%len(shapeInfo['points'])]]
        lines.append(line)
    return lines

def getStarPolygon(bounds, sides=3, rotation=0, order=2):
    polygonInfo = getPolygon(bounds, sides, rotation)
    polygonInfo['order'] = order
    if sides % order == 0:
        polygonInfo['degenerate'] = True
    else:
        polygonInfo['degenerate'] = False
    #set intersections
    return polygonInfo

def getStarLines(bounds, sides=3, rotation=0, order=2):
    polygonInfo = getPolygon(bounds, sides, rotation)
    lines = []
    #degenerate star
    if sides % order == 0:
        pass
    #regular star
    else:
        currIndex = 0
        for i in range(sides):
            print(currIndex)
            line = [polygonInfo['points'][currIndex], polygonInfo['points'][(currIndex + order) % sides]]
            lines.append(line)
            currIndex = (currIndex + order) % sides
    return lines
def getMidpoint(point1, point2):
    return ((point1[0]+point2[0])/2, (point1[1]+point2[1])/2)

def getDistance(point1, point2):
    return sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

def drawLines(draw, lines):
    for line in lines:
        draw.line(line)

#takes in a star/polygon and draws a circle that touches each point on the outside of the polygon
def drawOutline(draw, shapeInfo):
    draw.ellipse(shapeInfo['outlineBounds'])

#takes in a star/polygon and draws a cricle that touches each inside polygon line
def drawInscribe(draw, shapeInfo):
    draw.ellipse(shapeInfo['inscribeBounds'])

#takes in a star or polygon and draws lines from the points to the center
def drawSegments(draw, shapeInfo):
    lines = getSegmentLines(shapeInfo)
    drawLines(draw, lines)

#returns an list of coord pairs
def getSegmentLines(shapeInfo):
    #find the lines from each point to the center
    lines = []
    center = shapeInfo['center']
    for point in shapeInfo['points']:
        lines.append([point, center])
    return lines

## TODO
#draws stuff on each of the points
def drawOnPoints(draw):
    pass

if __name__ == '__main__':
    main()
