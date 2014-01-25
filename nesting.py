#Casey Cannon and Reyna Hulett

from pngIO import *
from math import *


def newPoints((a,b), (c,d)):
    img[a][b] = [0,0,0]
    img[c][d] = [255,0,0]

    l = sqrt((c-a)**2 + (d-b)**2)
    h = len(img)
    print "h is", h
    w = len(img[0])
    print "w is", w
    k = l * 1.0 / sqrt(w**2 + h**2)
    print "k is", k
    print "w**2 + h**2=", w**2 + h**2
    phi = asin(h / sqrt(w**2 + h**2)) - asin((d-b)/l)

    print "phi is", phi
    x = int(a + k*w*cos(phi))
    y = int(b - k*w*sin(phi))
    v = int(c - k*w*cos(phi))
    z = int(d + k*w*sin(phi))

    return (x,y,v,z)

def interpolate(img, x, y):
    px = x - int(x)
    py = y - int(y)
    newColor = [0,0,0]
    for color in range(3):
        u = img[int(y)][int(x)][color] + px * (img[int(y)][int(x)+1][color])
        v = img[int(y)+1][int(x)][color] + px * (img[int(y)+1][int(x)+1][color])
        newColor[color] = int(u + py *(v-u))
    return newColor

def main():
    img = getRGB('clipboard.png')
    h = len(img)
    w = len(img[0])
    fakeImg = [ [[0,1,0], [2,1,3]], [[2,1,3], [4,1,5]] ]
    print interpolate(fakeImg,0.5,0.5)


if __name__ == "__main__":
    main()