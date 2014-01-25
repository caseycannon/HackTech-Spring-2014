#Casey Cannon and Reyna Hulett

from pngIO import *
from math import *


def newCorners((a,b), (c,d), img):
    l = sqrt((c-a)**2 + (d-b)**2)
    h = len(img)
    w = len(img[0])
    k = l * 1.0 / sqrt(w**2 + h**2)
    phi = asin(h / sqrt(w**2 + h**2)) - asin((d-b)/l)

    x = int(a + k*w*cos(phi))
    y = int(b - k*w*sin(phi))
    v = int(c - k*w*cos(phi))
    z = int(d + k*w*sin(phi))

    return (x,y,v,z,k, phi)

def newPoints((a,b), hDist, vDist, phi, k, img):
    hDist = hDist - a
    vDist = vDist - b
    newY = hDist * sin(phi) + vDist * cos(phi)
    newX = hDist * cos(phi) - vDist * sin(phi)
    return (newX / k, newY / k)

def interpRGB(img, x, y):
    px = x - int(x)
    py = y - int(y)
    newColor = [0,0,0]
    for color in range(3):
        u = (1-px)*img[int(y)][int(x)][color] + px * (img[int(y)][int(x)+1][color])
        v = (1-px)*img[int(y)+1][int(x)][color] + px * (img[int(y)+1][int(x)+1][color])
        newColor[color] = int(u + py *(v-u))
    return newColor

def interp(y,p0,p1):
    slope = 1.0*(p1[0] - p0[0])/(p1[1] - p0[1])
    return p0[0] + slope * (y - p0[1])

#def isWithin(x,y,a,b,c,d):
#    if (a[0]==b[0] or a[0]==d[0]):
#        return True
#    count = 0
#    if interp(y,a,b)<x: count +=1
#    if interp(y,b,c)<x: count +=1
#    if interp(y,c,d)<x: count +=1
#    if interp(y,d,a)<x: count +=1
#    return count == 2

def isWithin(x,y,img):
    return (x>=0 and y>=0 and x <= len(img[0]) - 1 and y <= len(img)-1)

def nest(a, b, img):
    (x, y, w, z, k, phi) = newCorners(a,b,img)
    minX = min(x, w, a[0], b[0])
    minY = min(y, z, a[1], b[1])
    maxX = max(x, w, a[0], b[0])
    print "y, z, a[1], b[1]", y, z, a[1], b[1]
    maxY = max(y, z, a[1], b[1])

    for c in range(minX, maxX):
        for r in range(minY, maxY):
            (newC, newR) = newPoints(a, c, r, k, phi, img)
            if isWithin(newC, newR, img):
                #print "c, r", c, r
                img[r][c] = interpRGB(img,newC, newR)
    #nest((x,y), (w,z), img)
                

def main():
    img = getRGB('clipboard.png')
    nest((422,572), (100, 323), img)
    saveRGB(img, 'result.png')



if __name__ == "__main__":
    main()