from itertools import chain
from moviepy.editor import *
import imageio
import numpy
import math
import cv2
 
class Beanser():
    def __init__(self, numNeeded, maxRange):
        self._numNeeded = numNeeded
        self._maxRange = maxRange
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        

    numPossibles = 0
    schouldCont = True
    frame = 0
    bitsRange = math.ceil(math.log(maxRange, 2))
    tmp = 0
    count = 0
    sublist = []
    tempSublist = []
    outputList = []

    #==============================================================================
    # Przygotowanie klatek z filmu
    #==============================================================================

    def newImg():
        return_value, image = self.camera.read()
        img_name = "frame.png"
        cv2.imwrite(img_name, image)

    #==============================================================================
    # Sczytywanie liczb z klatek
    #==============================================================================

    numNeeded *= bitsRange

    while(schouldCont):

        newImg()

        image = imageio.imread('frame.png')
        imgHigth, imgWidth, imgChannel = image.shape

        # Wczytywanie do listy pomocniczej wartosci z calej klatki
        for i in range(0,imgHigth):
            for j in range(0,imgWidth):
                for k in range(0,imgChannel):
                    if(image[i][j][k] >= 2 and image[i][j][k] <= 253):
                        sublist.append(image[i][j][k] & 0b1)
                        numPossibles += 1
        frame += 1 
        if(numPossibles >= numNeeded):
            schouldCont = False

    # Obliczanie wielkosci macierzy kwadratowej
    square = math.floor(math.sqrt(numNeeded))

    for i in range(0,square*square):
        tempSublist.append(sublist[i])

    # Mieszanie macierzy
    tempSublist = numpy.array(tempSublist).reshape(square,square)
    transpose = tempSublist.T
    tempSublist = transpose.tolist()
    tempSublist = list(chain.from_iterable(tempSublist))

    # Jesli ilość liczb w macierzy kwadratowej jest niewystarczająca
    # dodawne sa liczby z ostatniej użytej klatki, od momentu uciecią jej
    # do macierzy kwadratowej
    if(square*square < numNeeded):
        for i in range(0, numNeeded - square*square):
            tempSublist.append(sublist[i+(square*square)])

    x = 0
    # Skladanie bitow w liczby z zakresu
    while(count < numNeeded/bitsRange):
        for j in range(0,bitsRange):
            valTmp = tempSublist[x]
            tmp = tmp | (valTmp << j)
            x += 1
        outputList.append(tmp)
        tmp = 0
        count += 1

    
    del(camera)



getBeans(10000, 256)
output = open("output.txt", "w")
    for element in outputList:
            output.write(str(element) + "\n")
    output.close()