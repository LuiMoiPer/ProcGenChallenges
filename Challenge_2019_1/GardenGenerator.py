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
    print(json.dumps(garden))

#The formmal grammar that describes a garden
def GetGrammar():
    grammar = {
        'Garden' : [
            '{"Garden" : {"Plots" : \[#Plots#\], "Features" : \[#Features#\]}}',
            '{"Garden" : {"Plots" : \[#Plots#\]}}'
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
    numPlots = len(g['Garden']['Plots'])
    numFeats = len(g['Garden'].get('Features', []))
    #print(f'Plots: {numPlots}\nFeats: {numFeats}\nTotal: {numPlots + numFeats}')

    #loop through each plot and get size
    for plot in g['Garden']['Plots']:
        plot['XDim'], plot['YDim'] = SetPlotSize(plot)

    #loop through each feature and get a size
    if g['Garden'].get('Features') != None:
        for feature in g['Garden']['Features']:
            feature['XDim'], feature['YDim'] = SetFeatureSize(feature)

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
    for plot in g['Garden']['Plots']:
        rooms.append(plot)
    for feature in g['Garden'].get('Features', []):
        rooms.append(feature)

    #set all the rooms to 0, 0
    for room in rooms:
        room['XLoc'], room['YLoc'] = 0, 0
        #print(room)

    #loop setup
    foundOverlap = True
    while foundOverlap == True:
        foundOverlap = False

        #room to be compared with the others
        for currRoom in rooms:
            for room in rooms:
                #if its the same room skip it
                if currRoom == room:
                    continue

                #if rooms overlap the move one
                if AreOverlapping(currRoom, room):
                    foundOverlap = True
                    '''
                    currRoom['XLoc'] += random.randrange(3) - 1
                    currRoom['YLoc'] += random.randrange(3) - 1
                    '''
                    if random.randrange(2) % 2 == 0:
                        currRoom['XLoc'] += random.randrange(3) - 1
                    else:
                        currRoom['YLoc'] += random.randrange(3) - 1
    #Shift everything so there are no negative x or y locations
    minX = math.inf
    minY = math.inf
    for room in rooms:
        if room['XLoc'] < minX:
            minX = room['XLoc']
        if room['YLoc'] < minY:
            minY = room['YLoc']

    #subtract the minX/Y room to shift it closer to 0,0
    for room in rooms:
        room['XLoc'] -= minX
        room['YLoc'] -= minY

def AreOverlapping(a, b):
    #check if a is to left of b
    if a['XLoc'] + a['XDim'] < b['XLoc']:
        return False
    #check if a is to right of b
    if a['XLoc'] > b['XLoc'] + b['XDim']:
        return False
    #check if a is above b
    if a['YLoc'] + a['YDim'] < b['YLoc']:
        return False
    #check if a is below b
    if a['YLoc'] > b['YLoc'] + b['YDim']:
        return False
    return True

def AreTouching(a, b):
    #check if a is to left of b
    if a['XLoc'] + a['XDim'] < b['XLoc']:
        return False
    #check if a is to right of b
    if a['XLoc'] > b['XLoc'] + b['XDim']:
        return False
    #check if a is above b
    if a['YLoc'] + a['YDim'] < b['YLoc']:
        return False
    #check if a is below b
    if a['YLoc'] > b['YLoc'] + b['YDim']:
        return False
    return True

def DrawGardenOutine(g):
    #get all rooms
    rooms = []
    for plot in g['Garden']['Plots']:
        rooms.append(plot)
    for feature in g['Garden'].get('Features', []):
        rooms.append(feature)

    maxX = -math.inf
    maxY = -math.inf
    #Find the max x and y
    for room in rooms:
        if room['XLoc'] + room['XDim'] > maxX:
            maxX = room['XLoc'] + room['XDim']
        if room['YLoc'] + room['YDim'] > maxY:
            maxY = room['YLoc'] + room['YDim']

    #make an image of size max x y
    scale = 100
    image = Image.new('RGB', (maxX*scale, maxY*scale), (255, 255, 255))


    #draw a rectangle for each room
    draw = ImageDraw.Draw(image)
    for room in rooms:
        topLeft = (room['XLoc'] * scale, room['YLoc'] * scale)
        botRight = ((room['XLoc'] + room['XDim']) * scale, (room['YLoc'] + room['YDim']) * scale)
        fill = (random.randrange(256), random.randrange(256), random.randrange(256))
        outline = (0, 0, 0)
        draw.rectangle([topLeft, botRight], fill, outline, 3)

    #save image
    image.save('layout.png')

if __name__ == "__main__":
    Main()
