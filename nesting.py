#Casey Cannon and Reyna Hulett

from pngIO import *
from math import *
count = 0

def newCorners((a,b), (c,d), img):
    """Given two opposite corners, Finds the two other corners, the phase ange and the
    scaling factor."""
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

def newPoints((a,b), hDist, vDist, phi, k):
    """Given the origin, rotation angle, and scaling factor of a subimage, finds the
    corresponding location in the original image."""
    hDist = hDist - a
    vDist = vDist - b
    #print "phi", phi
    newX = hDist * cos(phi) - vDist * sin(phi)
    newY = hDist * sin(phi) + vDist * cos(phi)
    return (newX / k, newY / k)

def getCorners((a,b), TLx, TLy, BRx, BRy, phi, lastH, lastW):
    """Given two opposite corners, a rotation angle, and a scaling factor, finds 
    location of the two corresponding corners in the next subimage."""
    newA = lastW * TLx * cos(phi) + lastH * TLy * sin(phi)
    newB = -lastW * TLx * sin(phi) + lastH * TLy * cos(phi)
    newC = lastW * BRx * cos(phi) + lastH * BRy * sin(phi)
    newD = -lastW * BRx * sin(phi) + lastH * BRy * cos(phi)
    return ((a + int(newA), b + int(newB)), (a + int(newC), b + int(newD)))

def interpRGB(img, x, y):
    """Given a floating point pixel location, linearly interpolates the RGB values between the
    4 surrounding pixels and rounds to give RGB values."""
    px = x - int(x)
    py = y - int(y)
    newColor = [0,0,0]
    for color in range(3):
        u = (1-px)*img[int(y)][int(x)][color] + px * (img[int(y)][int(x)+1][color])
        v = (1-px)*img[int(y)+1][int(x)][color] + px * (img[int(y)+1][int(x)+1][color])
        newColor[color] = int(u + py *(v-u))
    return newColor

def interp(y,p0,p1):
    """Finds the x value of the line through p0 and p1 at height y."""
    slope = 1.0*(p1[0] - p0[0])/(p1[1] - p0[1])
    return p0[0] + slope * (y - p0[1])

def isWithin(x,y,img):
    """Checks if x and y coordinates are within the bounds of the image."""
    return (x>=0 and y>=0 and x <= len(img[0]) - 1 and y <= len(img)-1)

def nest(a, b, TLx, TLy, BRx, BRy, img):
    """Nests an image inside of itself given two corners a and b."""
    if (b[1]-a[1])**2+(b[0]-a[0])**2 < 2:
        return img
    (x, y, w, z, k, phi) = newCorners(a,b,img)
    print "corner a", a, "corner b", b
    #img[a[1]][a[0]] =[0,255,0]
    #img[b[1]][b[0]] =[0,0,255]
    print "new corner xy", (x,y), "new corner wz", (w,z)
    #img[y][x] = [255,0,0]
    #img[z][w] = [255,255,0]
    minX = min(x, w, a[0], b[0])
    minY = min(y, z, a[1], b[1])
    maxX = max(x, w, a[0], b[0])
    maxY = max(y, z, a[1], b[1])
    count = 0
    for c in range(minX, maxX):
        for r in range(minY, maxY):
            (newC, newR) = newPoints(a, c, r, k, phi)
            if isWithin(newC, newR, img):
                #print "c, r, maxY", c, r, maxY
                img[r][c] = interpRGB(img,newC, newR)
                #count+=1
                #if count == 1000:
                #    saveRGB(img, "result.png")
                #    raw_input("Press Enter to continue...")
                #    count = 0
    #(new1, new2) = getCorners(a, TLx, TLy, BRx, BRy, phi, sqrt((a[0]-w)**2 + (a[1]-z)**2), sqrt((a[0]-x)**2 + (a[1]-y)**2))
    #print "new1, new2", new1, new2
    #nest(new1, new2, TLx, TLy, BRx, BRy, img)
    return img

def main():
    img = getRGB('clipboard.png')
    #img = [[[255 for color in range(3)] for row in range(500)] for col in range(889)]
    TLx = 100./len(img[0])
    TLy = 323./len(img)
    BRx = 422./len(img[0])
    BRy = 572./len(img)
    nest((100, 323), (422,572), TLx, TLy, BRx, BRy, img)
    #nest((33, 227), (483, 602), img)
    #nest((450,892), (490,870), img)
    saveRGB(img, 'result.png')

if __name__ == "__main__":
    main()