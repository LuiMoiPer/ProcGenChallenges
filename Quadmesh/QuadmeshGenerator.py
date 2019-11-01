#!/usr/bin/python3

from PIL import Image, ImageDraw
from Geometry import Polygon, Point

import pdb

foreground = 'hsb(5,0%,100%)'
background = 'hsb(5,0%,50%)'
img = Image.new('RGB', (1000, 1000), background)
draw = ImageDraw.Draw(img)

def main():
    points = [
        Point(300,100),
        Point(100,300),
        Point(600,100)
    ]
    poly = Polygon(points)

    draw.polygon(poly.verticiesAsTuples, outline=foreground)
    drawPoint(poly.centroid, size=10, fill='hsb(0,100%,100%)')
    img.show()

def drawPoint(point, size=50, fill=foreground):
    print(f'Point = {point}')
    p1 = point + Point(0,size/2)
    p2 = point - Point(0,size/2)
    p3 = point + Point(size/2,0)
    p4 = point - Point(size/2,0)

    draw.line([p1.asTuple(), p2.asTuple()],fill=fill)
    draw.line([p3.asTuple(), p4.asTuple()],fill=fill)

if __name__ == "__main__":
    main()
