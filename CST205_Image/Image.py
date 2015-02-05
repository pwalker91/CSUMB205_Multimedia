#!/usr/local/bin/python3
"""
-------------------------------------------------------------------------------
CST205_PIL.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This module will be used by CST 205 for image manipulation. It
            creates some classes that will use the PIL package (installed
            by calling 'pip3 install Pillow')

CLASSES-
    ..
-------------------------------------------------------------------------------
"""


# IMPORTS
import os
import sys
import subprocess
from tkinter.filedialog import (askdirectory, askopenfilename)
from PIL import Image
#END IMPORTS



#CLASS
class RGBPixel(object):
    __red = 0
    __green = 0
    __blue = 0
    x=0; y=0
    #DESC: Initializes the object
    def __init__(self,r=0,g=0,b=0, x=0, y=0):
        self.__red = r
        self.__green = g
        self.__blue = b
        self.checkVals()
        self.x = x
        self.y = y

    def checkVals(self):
        while (self.__red>255):
            self.__red = self.__red-256
        while (self.__green>255):
            self.__green = self.__green-256
        while (self.__blue>255):
            self.__blue = self.__blue-256

    def setRed(self, val):
        self.__red = val
        self.checkVals()

    def setGreen(self, val):
        self.__green = val
        self.checkVals()

    def setBlue(self, val):
        self.__blue = val
        self.checkVals()

    def __as_tuple(self):
        return (self.__red, self.__green, self.__blue)

    def __str__(self):
        return ("Pixel at ("+str(self.x)+","+str(self.y)+"): "+
                "RED="+str(self.__red)+", GREEN="+str(self.__green)+", BLUE="+str(self.__blue))
#END CLASS


#CLASS
class RGBImage(object):
    # ---------------------
    # Class Attributes
    inputFilename = ""
    outputFilename = ""
    mode = ""
    size = 0
    width = 0
    height = 0

    pixels = []
    # ---------------------

    #DESC: Initializes the object
    def __init__(self, filename="", saveTo=""):
        if not filename:
            self.inputFilename = askopenfilename( initialdir = os.path.expanduser("~"),
                                                title = "Select the FILE containing the raw data",
                                                multiple = False)
        '''askdirectory( initialdir = os.path.expanduser("~"),
                            title = "Select the FOLDER containing the raw data",
                            mustexist = True)'''
        self.inputFilename = filename
        if saveTo == "":
            self.outputFilename = filename.rsplit(".",1)[0]+"_v2"+filename.rsplit(".",1)[1]
        __myImage = Image.open(filename)
        self.mode = __myImage.mode
        if self.mode != "RGB":
            raise StandardError("This image must be made up of RGB pixels")
        self.width, self.height = __myImage.size
        self.size = self.width * self.height
        counter = 0
        for pixel in list(__myImage.getdata()):
            self.pixels.append(RGBPixel(*pixel, x=counter%self.width, y=int(counter/self.width)))
            counter+=1
        #END FOR
    #END DEF

    # DESC: ..
    #       ..
    def getPixel(self, x, y):
        if (x>self.width):
            raise ValueError("This pixel location is not within this picture bounds.")
        if (y>self.height):
            raise ValueError("This pixel location is not within this picture bounds.")
        if (x+(self.height*y) > self.size):
            raise ValueError("This pixel location is not within this picture bounds.")
        return self.pixels[x+(self.height*y)]
    #END DEF

    # DESC: ..
    #       ..
    def save(self, filename=""):
        if filename != "":
            self.outputFilename = filename
        Image.fromarray(self.pixels).save(self.outputFilename)
    #END DEF

    # DESC: ..
    #       ..
    def __str__(self):
        return ("RGB Image named "+self.inputFilename.split("/")[-1].split("\\")[-1]+"\n"+
                "Size is "+str(self.width)+"x"+str(self.height)+" pixels")
    #END DEF
#END CLASS
