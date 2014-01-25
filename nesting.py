from pngIO import *
from math import *

def test((a,b), (c,d)):
    img = [[[255 for color in range(3)] for row in range(300)] for col in range(600)]

    saveRGB(img, "test.png")
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

    img[y][x] = [0,255,0]
    img[z][v] = [0,0,255]    
    
    saveRGB(img, "clipboard-m.png")
