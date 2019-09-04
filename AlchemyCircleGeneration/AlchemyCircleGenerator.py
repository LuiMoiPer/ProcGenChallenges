
from AlchemyCircle import AlchemyCircle as AC
from PIL import Image, ImageDraw
import random

foreground = 'hsb(5,0%,100%)'
background = 'hsb(5,0%,50%)'
img = Image.new('RGB', (1000, 1000), background)
draw = ImageDraw.Draw(img)

def main():
    for i in range(50):
        generateCircle()
        img.save(f'GeneratedAlchemyCircles/{i}.png')
        draw.rectangle([(0,0), (1000, 1000)], fill=background)

def generateCircle():
    #Choose how many layers there will be
    #for each layer
        #choose features
        #draw features
        #use the layer features to influence next layers

    layers = random.randint(1, 6)
    i = 0
    circleParams = {
        'center' : (500, 500),
        'radius' : 400,
        'sides' : random.randint(3, 8),
        'order' : 1
    }
    while i < layers:
        currCircle = AC(**circleParams)
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
            if bool(random.getrandbits(1)):
                draw.ellipse(currCircle.getOutlineBounds(), outline=foreground)
            else:
                draw.ellipse(currCircle.getOutlineBounds(), outline=foreground, fill=background)

        if features['star']:
            #choose which order the star is
            currCircle.order = random.randint(1, currCircle.sides+1)

        if features['polygon']:
            #draw the polygon
            for line in currCircle.lines:
                draw.line(line)

        if features['segmentLines']:
            #draw the segment lines
            for line in currCircle.segmentLines:
                draw.line(line)

        if features['inline']:
            #choose wether there is a fill or not
            if bool(random.getrandbits(1)):
                draw.ellipse(currCircle.getInlineBounds(), outline=foreground)
            else:
                draw.ellipse(currCircle.getInlineBounds(), outline=foreground, fill=background)

        if features['nodes']:
            #choose if the nodes are filled
            #choose if the nodes are rotated towards the center
            drawBackground = bool(random.getrandbits(1))
            fillNodes = bool(random.getrandbits(1))
            rotateToCenter = bool(random.getrandbits(1))

            for point in currCircle.points:
                nodeCircle = AC(center=point, radius=25, sides=random.randint(3,currCircle.sides))

                if rotateToCenter:
                    nodeCircle.rotation = AC.getAngle(nodeCircle.center, currCircle.center)

                if drawBackground:
                    draw.ellipse(nodeCircle.getOutlineBounds(), outline=foreground, fill=background)
                else:
                    draw.ellipse(nodeCircle.getOutlineBounds(), outline=foreground)

                if fillNodes:
                    for line in nodeCircle.lines:
                        draw.line(line)


        #update cricle params
        circleParams['sides'] = random.randint(3, 8)
        circleParams['order'] = 1
        if bool(random.getrandbits(1)):
            circleParams['radius'] = random.randint(int(currCircle.radius * 0.25), int(currCircle.radius + 25))
        elif bool(random.getrandbits(1)):
            circleParams['radius'] = currCircle.inlineRadius
        else:
            circleParams['radius'] = currCircle.radius

        i+=1

if __name__ == '__main__':
    main()
