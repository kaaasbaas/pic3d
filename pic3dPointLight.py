import math 
from PIL import Image
import sys

input_filename = sys.argv[1]
output_filename = input_filename.split('.')[0] + '-3dpl.png'
img = Image.open(input_filename)

if type(img.getpixel((0, 0))) == int:
    values = [
        [
            img.getpixel((x, y))
            for x in range(img.width)
        ]
        for y in range(img.height)
    ]
else:
    values = [
        [
            sum(img.getpixel((x, y)))
            for x in range(img.width)
        ]
        for y in range(img.height)
    ]

def pixelOrder(values, origin):
    distanceList = []
    for x in range (len(values)):
        for y in range (len(values[0])):
            distanceList.append((abs(x - origin[0]) + abs(y - origin[1]), x, y))
    
    distanceList = sorted(distanceList)
    
    return [(c[1], c[2]) for c in distanceList]

def normalized(values):
    max_val = max(v for row in values for v in row)
    min_val = min(v for row in values for v in row)

    return [
        [
            (v - min_val) / (max_val - min_val)
            for v in row
        ]
        for row in values
    ]

values = normalized(values)

def heightmap(values, origin, orderList, inc):
    hm = values
    hm[max(0, min(origin[0], len(values) - 1))][max(0, min(origin[1], len(values[0]) - 1))] = 0

    for c in orderList:
        x = c[0]
        y = c[1]
        if(x == origin[0] and y == origin[1]):
            x = y
        else:
            if(x != origin and y):
                dx = origin[0] - x
                dy = origin[1] - y

                fx = 0
                fy = 0

                if dx > 0:
                    if x == len(values) - 1:
                        fx = 0
                    else:
                        fx = hm[x + 1][y]
                elif dx < 0:
                    if x == 0:
                        fx = 0
                    else:
                        fx = hm[x - 1][y]
                if dy > 0:
                    if y == len(values[0]) - 1:
                        fy = 0
                    else:
                        fy = hm[x][y + 1]
                elif dy < 0:
                    if y == 0:
                        fy = 0
                    else:
                        fy = hm[x][y - 1]

                if (abs(dx) < 10 and abs(dy) < 10):
                    print ("(" + str(dx) + ", " + str(dy) + ") = " + str(hm[x][y]) + " = " + str(values[x][y]) + " + " + str((fx * abs(dx) + fy * abs(dy)) / (abs(dx) + abs(dy))) + " + " + str(inc))

                hm[x][y] = values[x][y] + (fx * abs(dx) + fy * abs(dy)) / (abs(dx) + abs(dy)) + inc
    return hm
            


def row2heightmap(l, inc):
    total = sum(l)
    res = [0]
    s = 0
    for x in l:
        s += x + inc
        res.append(s)
    offset = -s/2
    return [r+offset for r in res]

origin = (math.floor(len(values) * 10), math.floor(len(values[0]) / 2))

inc = -sum(v for row in values for v in row) / len(values) / len(values[0])
height_map = heightmap(values, origin, pixelOrder(values, origin), inc)
height_map = normalized(height_map)

out_img = Image.new('RGB', (len(height_map[0]), len(height_map)))
for y, row in enumerate(height_map):
    for x, h in enumerate(row):
        c = int(255.5*h)
        out_img.putpixel((x, y), (c,c,c))

out_img.save(output_filename)
