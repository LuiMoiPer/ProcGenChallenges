import tracery
import json
import random
import math
from PIL import Image, ImageDraw

def Main():

    #define the grammar
    gardenGrammar = GetGrammar()

    #generate the garden in json
    gardenGen = tracery.Grammar(gardenGrammar)
    garden = gardenGen.flatten('#Garden#')
    garden = json.loads(garden)

    #make the plot and feature "rooms"
    SetRoomSizes(garden)

    #set up the room positions
    SetRoomPositions(garden)

    #make a graphic
    #DrawGardenOutine(garden)

    #export the layout
    print(json.dumps(garden, indent = 4))
    file = open('Garden.json', 'w')
    file.write(json.dumps(garden, indent = 4))
    file.close()


#The formmal grammar that describes a garden
def GetGrammar():
    grammar = {
        'Garden' : [
            '{"Plots" : \[#Plots#\], "Features" : \[#Features#\]}',
            '{"Plots" : \[#Plots#\]}'
        ],

        'Plots' : [
            '#Plot#, #Plots#',
            '#Plot#, #Plots#',
            '#Plot#'
        ],

        'Plot' : [
            '{"PlotType" : "Flowers", "Flowers" : \[#Flowers#\]}',
            '{"PlotType" : "Crops", "Crops" : #Crop#}',
            '{"PlotType" : "Bush", "Bush" : #Bush#}'
        ],

        'Flowers' : [
            '#Flower#, #Flowers#',
            '#Flower#, #Flowers#',
            '#Flower#'
        ],

        'Flower' : '{"Height" : #Height#, "BulbType" : #BulbType#, "Color" : #Color#}',

        'Height' : [
            '"short"',
            '"med"',
            '"tall"'
        ],

        'BulbType' : [
            '"closed"',
            '"star"',
            '"round"'
        ],

        'Color' : [
            '"red"',
            '"blue"',
            '"white"',
            '"yellow"',
            '"purple"',
            '"orange"',
            '"pink"'
        ],

        'Crop' : [
            '"tomatoes"',
            '"watermelon"',
            '"corn"',
            '"pumpkin"',
            '"grass"'
        ],

        'Bush' : [
            '{"BerryColor" : "None"}',
            '{"BerryColor" : #Color#}'
        ],

        'Features' : [
            '#Feature#, #Features#',
            '#Feature#'
        ],

        'Feature' : [
            '{"FeatureType" : "Gazebo"}',
            '{"FeatureType" : "Fountain"}',
            '{"FeatureType" : "Pond"}',
            '{"FeatureType" : "Statue"}',
            '{"FeatureType" : "Tree"}',
            #'{"FeatureType" : "Maze"}',
        ]
    }

    return grammar

def PrimeFactors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

#Choose how big the room is going to be
def SetRoomSizes(g):
    numPlots = len(g['Plots'])
    numFeats = len(g.get('Features', []))
    #print(f'Plots: {numPlots}\nFeats: {numFeats}\nTotal: {numPlots + numFeats}')

    #loop through each plot and get size
    for plot in g['Plots']:
        plot['Size'] = {}
        plot['Size']['x'], plot['Size']['y'] = SetPlotSize(plot)

    #loop through each feature and get a size
    if g.get('Features') != None:
        for feature in g['Features']:
            feature['Size'] = {}
            feature['Size']['x'], feature['Size']['y'] = SetFeatureSize(feature)

#Takes in a plot and adds an XDim and YDim
def SetPlotSize(p):
    #Flowers
    if p['PlotType'] == 'Flowers':
        #get dimmensions that can hold set ammount of flowers
        dims = GetDimensions(len(p['Flowers']))
        return dims[0], dims[1]

    #Crops
    elif p['PlotType'] == 'Crops':
        #pick plot size at random
        area = random.randrange(0,8) + 1
        #get dimensions
        dims = GetDimensions(area)
        return dims[0], dims[1]

    #Bush
    elif p['PlotType'] == 'Bush':
        #pick plot size at random
        area = random.randrange(0,8) + 1
        #get dimensions
        dims = GetDimensions(area)
        return dims[0], dims[1]

    else:
        print('NOT HADLED PLOT TYPE')
    return 1, 1

#Takes in a feature and adds an XDim and YDim
def SetFeatureSize(f):
    #Gazebo
    if f['FeatureType'] == 'Gazebo':
        #make a list of all possible dimensions
        possibleDims = [
            [2, 2],
            [2, 3],
            [3, 3]
        ]

        #Choose a set of dimmensions at random and shuffle them
        dims = random.choice(possibleDims)
        random.shuffle(dims)

        return dims[0], dims[1]

    #Fountain#
    elif f['FeatureType'] == 'Fountain':
        #make a list of all possible dimensions
        possibleDims = [
            [2, 2],
            [1, 1]
        ]

        #Choose a set of dimmensions at random and shuffle them
        dims = random.choice(possibleDims)
        random.shuffle(dims)

        return dims[0], dims[1]

    #Pond
    elif f['FeatureType'] == 'Pond':
        #make a list of all possible dimensions
        possibleDims = [
            [2, 2],
            [2, 3],
            [3, 3]
        ]

        #Choose a set of dimmensions at random and shuffle them
        dims = random.choice(possibleDims)
        random.shuffle(dims)

        return dims[0], dims[1]

    #Statue
    elif f['FeatureType'] == 'Statue':
        #make a list of all possible dimensions
        possibleDims = [
            [1, 1],
            [1, 2],
            [2, 2]
        ]

        #Choose a set of dimmensions at random and shuffle them
        dims = random.choice(possibleDims)
        random.shuffle(dims)

        return dims[0], dims[1]

    #Tree
    elif f['FeatureType'] == 'Tree':
        #make a list of all possible dimensions
        possibleDims = [
            [1, 1],
            [2, 2]
        ]

        #Choose a set of dimmensions at random and shuffle them
        dims = random.choice(possibleDims)
        random.shuffle(dims)

        return dims[0], dims[1]

    else:
        print("NOT HANDLED FEATURE TYPES")
    #Maze
    return 1,1
#pass in an area and it find XDim and YDim
def GetDimensions(a):
    dims = PrimeFactors(a)
    #Make the list into only 2 dimensions
    while len(dims) < 2:
        dims.append(1)
    while len(dims) > 2:
        #pop 2 at random
        n1 = dims.pop(random.randrange(len(dims)))
        n2 = dims.pop(random.randrange(len(dims)))

        #multiply the two and append one
        dims.append(n1 * n2)

    #shuffle x and y so we get a mix of orientations
    random.shuffle(dims)
    return dims
#Decide final xy for the room
def SetRoomPositions(g):
    #get all the rooms
    rooms = []
    for plot in g['Plots']:
        rooms.append(plot)
    for feature in g.get('Features', []):
        rooms.append(feature)

    #set all the rooms to 0, 0
    for room in rooms:
        room['Location'] = {}
        room['Location']['x'], room['Location']['y'] = 0, 0
        room['Color'] = (127, 127, 127)
        #print(room)

    #loop setup
    i = 0
    foundOverlap = True
    while foundOverlap == True:
        foundOverlap = False

        #room to be compared with the others
        for currRoom in rooms:

            #set currRoom to be red
            currRoom['Color'] = (255, 100, 100)

            for room in rooms:
                #if its the same room skip it
                if currRoom == room:
                    continue

                #set the room color to blue
                room['Color'] = (100, 100, 255)

                #if rooms overlap the move one
                if AreOverlapping(currRoom, room):
                    foundOverlap = True
                    '''
                    if random.randrange(2) % 2 == 0:
                        room['XLoc'] += random.choice([1, -1])
                    else:
                        room['YLoc'] += random.choice([1, -1])
                    '''
                    # find the distance to the overlapping block
                    xDist, yDist = GetDistance(currRoom, room)

                    #move it 1 unit away in the axis it is closest
                    if xDist < yDist:
                        room['Location']['x'] -= math.copysign(1, xDist)
                    else:
                        room['Location']['y'] -= math.copysign(1, yDist)
                    ShiftPositions(g)
                    DrawGardenOutine(g, f'./output/{str(i)}')
                    i += 1

                #reset the room color
                room['Color'] = (127, 127, 127)

            #reset the room color
            currRoom['Color'] = (127, 127, 127)

    for room in rooms:
        room['Location']['x'] = float(room['Location']['x'])
        room['Location']['y'] = float(room['Location']['y'])
        room['Size']['x'] = float(room['Size']['x'])
        room['Size']['y'] = float(room['Size']['y'])
        del room['Color']

def AreOverlapping(a, b):
    #check if a is to left of b
    if a['Location']['x'] + a['Size']['x'] < b['Location']['x']:
        return False
    #check if a is to right of b
    if a['Location']['x'] > b['Location']['x'] + b['Size']['x']:
        return False
    #check if a is above b
    if a['Location']['y'] + a['Size']['y'] < b['Location']['y']:
        return False
    #check if a is below b
    if a['Location']['y'] > b['Location']['y'] + b['Size']['y']:
        return False
    return True

def AreTouching(a, b):
    #check if a is to left of b
    if a['Location']['x'] + a['Size']['x'] <= b['Location']['x']:
        return False
    #check if a is to right of b
    if a['Location']['x'] >= b['Location']['x'] + b['Size']['x']:
        return False
    #check if a is above b
    if a['Location']['y'] + a['Size']['y'] <= b['Location']['y']:
        return False
    #check if a is below b
    if a['Location']['y'] >= b['Location']['y'] + b['Size']['y']:
        return False
    return True

def DrawGardenOutine(g, filename = 'layout'):
    #get all rooms
    rooms = []
    for plot in g['Plots']:
        rooms.append(plot)
    for feature in g.get('Features', []):
        rooms.append(feature)

    maxX = -math.inf
    maxY = -math.inf
    #Find the max x and y
    for room in rooms:
        if room['Location']['x'] + room['Size']['x'] > maxX:
            maxX = room['Location']['x'] + room['Size']['x']
        if room['Location']['y'] + room['Size']['y'] > maxY:
            maxY = room['Location']['y'] + room['Size']['y']

    #make an image of size max x y
    scale = 100
    image = Image.new('RGB', (int(maxX*scale), int(maxY*scale)), (255, 255, 255))


    #draw a rectangle for each room
    draw = ImageDraw.Draw(image)
    for room in rooms:
        topLeft = (room['Location']['x'] * scale, room['Location']['y'] * scale)
        botRight = ((room['Location']['x'] + room['Size']['x']) * scale, (room['Location']['y'] + room['Size']['y']) * scale)
        fill = (room['Color'])
        outline = (0, 0, 0)
        draw.rectangle([topLeft, botRight], fill, outline, 3)

    #save image
    image.save(filename,'png')

#Shift everything so there are no negative x or y locations
def ShiftPositions(g):
    #get all the rooms
    rooms = []
    for plot in g['Plots']:
        rooms.append(plot)
    for feature in g.get('Features', []):
        rooms.append(feature)

    #Shift everything so there are no negative x or y locations
    minX = math.inf
    minY = math.inf
    for room in rooms:
        if room['Location']['x'] < minX:
            minX = room['Location']['x']
        if room['Location']['y'] < minY:
            minY = room['Location']['y']

    #subtract the minX/Y room to shift it closer to 0,0
    for room in rooms:
        room['Location']['x'] -= minX
        room['Location']['y'] -= minY

def GetDistance(a, b):
    aCenter = [
        a['Location']['x'] + a['Size']['x'] / 2,
        a['Location']['y'] + a['Size']['y'] / 2,
    ]

    bCenter = [
        b['Location']['x'] + b['Size']['x'] / 2,
        b['Location']['y'] + b['Size']['y'] / 2,
    ]

    return aCenter[0] - bCenter[0], aCenter[1] - bCenter[1]
if __name__ == "__main__":
    Main()
