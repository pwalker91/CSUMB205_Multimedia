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

try:
    from PIL import Image
except ImportError:
    subprocess.check_call("pip3 install Pillow", shell = True)
    from PIL import Image
#END TRY/EXCEPT
#END IMPORTS



#CLASS
class RGBPixel(object):
    r = 0; g = 0; b = 0
    x=0; y=0
    #DESC: Initializes the object
    def __init__(self,r=0,g=0,b=0, x=0, y=0):
        self.r = r
        while (self.r>255):
            self.r = self.r-256
        self.g = g
        while (self.g>255):
            self.g = self.g-256
        self.b = b
        while (self.b>255):
            self.b = self.b-256
        self.x = x
        self.y = y

    def checkVals(self):
        while (self.r>255):
            self.r = self.r-256
        while (self.g>255):
            self.g = self.g-256
        while (self.b>255):
            self.b = self.b-256

    def setR(self, val):
        self.r = val
        while (self.r>255):
            self.r = self.r-256

    def setG(self, val):
        self.g = val
        while (self.g>255):
            self.g = self.g-256

    def setB(self, val):
        self.b = val
        while (self.b>255):
            self.b = self.b-256

    def as_tuple(self):
        return (self.r, self.g, self.b)

    def __str__(self):
        return ("Pixel at ("+str(self.x)+","+str(self.y)+"): "+
                "RED="+str(self.r)+", GREEN="+str(self.g)+", BLUE="+str(self.b))
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

    myPixels = []
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
        self.outputFilename = saveTo
        __myImage = Image.open(filename)
        self.mode = __myImage.mode
        if self.mode != "RGB":
            raise StandardError("This image must be made up of RGB pixels")
        self.width, self.height = __myImage.size
        self.size = self.width * self.height
        counter = 0
        for pixel in list(__myImage.getdata()):
            self.myPixels.append(RGBPixel(*pixel, x=counter%self.width, y=int(counter/self.width)))
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
        return self.myPixels[x+(self.height*y)]
    #END DEF

    # DESC: ..
    #       ..
    def save(self, filename=""):
        if filename != "":
            self.outputFilename = filename
        Image.fromarray(self.myPixels).save(self.outputFilename)
    #END DEF

    # DESC: ..
    #       ..
    def __str__(self):
        return ("RGB Image named "+self.inputFilename.split("/")[-1].split("\\")[-1]+"\n"+
                "Size is "+str(self.width)+"x"+str(self.height)+" pixels")
    #END DEF
#END CLASS
