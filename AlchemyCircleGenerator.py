
from AlchemyCircle import AlchemyCircle as AC
from PIL import Image, ImageDraw
import random

img = Image.new('RGB', (1000, 1000), 'hsb(5,0%,50%)')
draw = ImageDraw.Draw(img)

def main():
    pass

def drawLines(lines):
    for line in lines:
        draw.line(line)

def generateCircle():
    #Choose how many layers there will be
    #for each layer
        #choose features
        #draw features
        #use the layer features to influence next layers

    layers = random.randint(1, 6)
    i = 0
    while i < layers:
        features = {
            'inline' : bool(random.getrandbits(1)),
            'nodes' : bool(random.getrandbits(1)),
            'outline' : bool(random.getrandbits(1)),
            'polygon' : bool(random.getrandbits(1)),
            'segmentLines' : bool(random.getrandbits(1)),
            'star' : bool(random.getrandbits(1))
        }

        if features['outline']:
            #choose if the oufline has a fill or not
            #draw the outline
            pass
        elif features['star']:
            #choose which order the star is
            pass
        elif features['polygon']:
            #draw the polygon
            pass
        elif features['segmentLines']:
            #draw the segment lines
            pass
        elif features['inline']:
            #choose wether there is a fill or not
            pass
        else features['nodes']:
            #choose what points the nodes will be on
            #choose if the nodes are filled
            #choose if the nodes are rotated towards the center
            pass


def recursiveInnerCircles(circle, minRadius):
    import random
    #draw a circle
    if random.randint(0, 9) % 2 == 0:
        draw.ellipse(circle.getOutlineBounds(), outline='hsb(0,0%,100%)', fill='hsb(5,0%,50%)')
    drawLines(circle.lines)

    if circle.inlineRadius >= minRadius:
        circleParams = {
            'center': circle.center,
            'minRadius': circle.inlineRadius,
            'maxRadius': circle.inlineRadius,
            'maxRotation': 0
        }

        #make stuff on intersections
        for intersection in circle.intersections:
            intersectionCircleParams = {
                'center': intersection,
                'minRadius': minRadius,
                'maxRadius': AC.getDistance(circle.intersections[0], circle.intersections[1]) / 2,
                'minRotation': AC.getAngle(intersection, circle.center),
                'maxRotation': AC.getAngle(intersection, circle.center)
            }
            recursiveInnerCircles(AC.random(**intersectionCircleParams), minRadius)

        recursiveInnerCircles(AC.random(**circleParams), minRadius)

if __name__ == '__main__':
    main()
