#!/usr/local/bin/python3
"""
-------------------------------------------------------------------------------
CST205_PIL.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This module will be used by CST 205 for image manipulation. It
            creates some classes that will use the PIL package (installed
            by calling 'pip3 install Pillow')

CLASSES-
    rgbPixel
    rgbImage
-------------------------------------------------------------------------------
"""


# IMPORTS
import os
#import sys
#import subprocess
from numpy import asarray, uint8
from tkinter.filedialog import (askdirectory, askopenfilename)
from PIL import Image
#END IMPORTS



#CLASS
class rgbPixel(object):
    __red = 0
    __green = 0
    __blue = 0
    __x=0
    __y=0

    def __init__(self, *args):
        """
        Object initialization
        ARGS:
            self    this Object
            (r,g,b) Tuple/List of pixel's color's R,G, and B values
                or
            r       A pixel value for the Red aspect
            g       A pixel value for the Green aspect
            b       A pixel value for the Blue aspect

            (x,y)   Tuple/List of the pixel's X and Y coordinate
                or
            x       The X-part of the this pixel's location within the picture
            y       The Y-part of the this pixel's location within the picture
        """
        self.setColor(*args)
        #Determining whether the color was passed in as a list.tuple, or as 3 separate values
        if not isinstance(args[0], list) and not isinstance(args[0], tuple):
            if len(args)<4:
                raise ValueError("You must pass in at least three values to set this pixel's color to.")
            if not all([isinstance(arg, int) for arg in args[:3]]):
                raise ValueError("You must pass in at least three integer values to set this pixel's color to.")
            self.setColor(args[:3])
            args = args[3:]
        else:
            #If setColor() did not raise an error, then we know that there were 3 separate values
            self.setColor(args[0])
            args = args[1:]
        #END IF/ELSE
        #Checking that the coordinate are viable
        if not isinstance(args[0], list) and not isinstance(args[0], tuple):
            if len(args)<2:
                raise ValueError("You must pass in at least two values to set this pixel's coordinate to.")
            if not all([isinstance(arg, int) for arg in args[:2]]):
                raise ValueError("You must pass in at least two integer values to set this pixel's coordinate to.")
            coord = tuple(args[:2])
        else:
            if len(args[0])<2:
                raise ValueError("You must pass in at least two values to set this pixel's coordinate to.")
            if not all([isinstance(arg, int) for arg in args[0][:2]]):
                raise ValueError("You must pass in at least two integer values to set this pixel's coordinate to.")
            coord = tuple(args[0][:2])
        #END IF/ELSE
        self.__x, self.__y = coord

    def _checkVals(func):
        """
        A decorator that will make sure that the arguments passed are viable.
        The arguments we are expected are "self", and an integer value between
         0 and 255.
        """
        def wrapper(*args, **kwargs):
            if not isinstance(args[1], int):
                raise ValueError("This function requires two positional arguments: ARG #2 must be an integer value.")
            #Casting args to a list so that we can modify the values (args was originally
            # a tuple, which is immutable)
            args = list(args)
            #This will make sure that the value is between 0 and 255, by iteratively
            # adding or subtracting 256
            while args[1] > 255 or args[1] < 0:
                if args[1] < 0:     args[1] += 256
                elif args[1] > 255: args[1] -= 256
            #END WHILE
            #Casting args back to being a tuple
            args = tuple(args)
            return func(*args, **kwargs)
        return wrapper
    #END DEF

    @_checkVals
    def setRed(self, val):
        self.__red = val
    def getRed(self):
        return self.__red

    @_checkVals
    def setGreen(self, val):
        self.__green = val
    def getGreen(self):
        return self.__green

    @_checkVals
    def setBlue(self, val):
        self.__blue = val
    def getBlue(self):
        return self.__blue

    def setColor(self, *args):
        """
        Sets this pixel's R,G, and B values to the given values
        ARGS:
            (R,G,B)     Tuple/List of three integers
                or
            R           Integer value, the red value of the color
            G           Integer value, the green value of the color
            B           Integer value, the blue value of the color
        """
        if not isinstance(args[0], list) and not isinstance(args[0], tuple):
            if len(args)<3:
                raise ValueError("You must pass in at least three values to set this pixel's color to.")
            color = list(args[:3])
        else:
            if len(args[0])<3:
                raise ValueError("You must pass in at least three values to set this pixel's color to.")
            color = list(args[0][:3])
        #END IF/ELSE
        for i in range(3):
            if not isinstance(color[i], int):
                raise ValueError("You must pass in at least three integer values to set this pixel's color to.")
            while color[i]<0 or color[i]>256:
                if color[i]<0:      color[i]+=256
                elif color[i]>255:  color[i]-=256
            #END WHILE
        #END FOR
        color = tuple(color)
        self.__red, self.__green, self.__blue = color
        return 0
    #END DEF
    def getColor(self):
        return self._as_tuple()

    def getX(self):
        return self.__x
    def getY(self):
        return self.__y

    def _as_array(self):
        """Returns the pixel's RGB values in a list format"""
        return [self.__red, self.__green, self.__blue]
    def _as_tuple(self):
        """Returns the pixel's RGB values in a tuple format"""
        return (self.__red, self.__green, self.__blue)

    def cdist(self, **kwargs):
        """
        Gets the color distance between this pixel and a specified color or pixel object
        ARGS:
            color   tuple, 3 integer values where 0<=x<=255
            pixel   an rgbPixel object
        RETURNS:
            A Float, that is this pixel's color's distance to the given rgbPixel or
             color tuple.
            A negative number means that this pixel will likely be lighter, while
             a positive number means that this pixel will likely be darker
        """
        if not any( [elem in kwargs for elem in ["color", "pixel"]] ):
            raise KeyError("You must pass either a color or pixel through the keywords 'color' or 'pixel'")
        if "color" in kwargs:
            if not (isinstance(kwargs['color'], tuple) or isinstance(kwargs['color'], list)) \
                    and len(kwargs['color']) != 3:
                raise ValueError("You must give an RGB value as a tuple (r,g,b) to 'color'")
        elif "pixel" in kwargs:
            if (self.__class__ != kwargs['pixel'].__class__):
                raise ValueError("You must give an rgbPixel object to 'pixel'")
        #END IF/ELIF
        if "color" in kwargs:
            givenR, givenG, givenB = kwargs['color']
        elif "pixel" in kwargs:
            givenR, givenG, givenB = kwargs['pixel']._as_tuple()
        rDist = givenR-self.__red
        gDist = givenG-self.__green
        bDist = givenB-self.__blue
        return ((rDist+gDist+bDist)/3.0)
    #END DEF

    def ldist(self, pixel):
        """
        Returns the length distance between two rgbPixels according to their
         X and Y values.
        """
        if not isinstance(pixel, self.__class__):
            raise ValueError("You must pass an rgbPixel to this function")
        xDist = pixel.getX()-self.__x
        yDist = pixel.getY()-self.__y
        from math import sqrt
        return sqrt(xDist**2 + yDist**2)
    #END DEF

    def __str__(self):
        """Returns a string representation of this object"""
        return ("Pixel at ({},{}): ".format(self.__x, self.__y)+
                "RED={}, GREEN={}, BLUE={}".format(self.__red, self.__green, self.__blue))
    #END DEF
#END CLASS



#CLASS
class rgbImage(object):
    # ---------------------
    # Class Attributes
    inputFilename = ""
    outputFilename = ""

    __myImage = None
    pixels = []

    height = 0
    width = 0
    # ---------------------

    def __init__(self, filename="", saveTo="", blank=False, width=100, height=100):
        """
        Object initialization
        ARGS:
            self        this Object
            filename    String, the location of the picture
            saveTo      String, the location that this picture will be saved to
            blank       Boolean, whether this image should be a blank image
                width   Integer, the width of the blank image
                height  Integer, the height of the blank image
        """
        if not blank:
            if not filename:
                self.inputFilename = askopenfilename( initialdir = os.path.expanduser("~"),
                                            title = "Select the FILE containing the raw data",
                                            multiple = False)
            else:
                self.inputFilename = os.path.abspath(filename)
                if not os.path.isfile(self.inputFilename) or \
                        self.inputFilename.split(".")[-1].lower() not in ["jpg","jpeg","png","gif"]:
                    raise ValueError("You must pass in a legitimate picture file")
            #END IF/ELSE
            if not saveTo:
                self.outputFilename = (self.inputFilename.rsplit(".",1)[0] + "_v2." +
                                        self.inputFilename.rsplit(".",1)[1])
            else:
                self.outputFilename = os.path.abspath(saveTo)
            #END IF/ELSE
            if os.path.isfile(self.outputFilename):
                shortOutput = self.outputFilename.split("/")[-1].split("\\")[-1]
                print("{} will be overwritten if this file is saved. ".format(shortOutput)+
                        "Consider saving to another location."
                    )
            #END IF
            self.__myImage = Image.open(self.inputFilename)
        else:
            self.__myImage = Image.new("RGB", (width, height))
        #END IF/ELSE

        #Calls self.reset(), as the reset function does what we want to do initially
        self.reset()

        #Setting some other useful variables for users
        self.width, self.height = self.__myImage.size
    #END DEF

    def getPixel(self, *args):
        """
        Gets an rgbPixel object at the specified (x,y) coordinate
        ARGS:
            self    this Object
            x       The X coordinate of the pixel
            y       The Y coordinate of the pixel
                or
            (x,y)   The X and Y coordinate within a tuple or list
        RETURNS:
            rgbPixel object
        RAISES:
            ValueError - 'x' or 'y' is out of the picture's bounds
        """
        #Getting the X and Y from the passed arguments
        if (isinstance(args[0], tuple) or isinstance(args[0], list)) and len(args[0])>1:
            x,y = args[0]
            if not(isinstance(x,int) and isinstance(y,int)):
                raise ValueError("The first two elements of the tuple you passed were not integers")
        elif (isinstance(args[0],int) and isinstance(args[1],int)):
            if (args[0]>self.width):
                raise ValueError("This pixel location is not within this picture bounds.")
            if (args[1]>self.height):
                raise ValueError("This pixel location is not within this picture bounds.")
            x = args[0]
            y = args[1]
        else:
            raise ValueError("You must either pass in a 2-tuple of integers, or two integers")
        return self.pixels[y][x]
    #END DEF

    def getAllPixels(self):
        """Converts this object's 'pixels' attribute into a 1-dimensional array"""
        allPixels = []
        for row in self.pixels:
            for pixel in row:
                allPixels.append(pixel)
        return allPixels
    #END DEF

    def save(self, filename="", forceOverwrite=False):
        """
        This will save the current object to a specified location
        ARGS:
            self            this Object
            filename        OPTIONAL. String, the location to be save to.
            forceOverwrite  OPTIONAL. Boolean, whether to force overwrite of file
                             at location 'filename' or 'self.outputFilename'
        RETURNS:
            none
        RAISES:
            none.
            Will ask user if they wish to overwrite a file if it exists at the given
             location in filename, or at self.outputFilename
        """
        if filename:
            self.outputFilename = os.path.abspath(filename)
        if os.path.isfile(self.outputFilename) and not forceOverwrite:
            overwrite = input( "{} will be overwritten. Continue? (y/n) ".format(self.outputFilename) )
            if overwrite.lower() != "y":
                return
        #END IF
        #array needs to be an array of rows, each row needs to be an array of
        # pixels, and each pixel an array of pixel values (R,G,B)
        img_to_array = asarray(self.__as_array())
        Image.fromarray(img_to_array).save(self.outputFilename)
        print("File saved at {}".format(self.outputFilename))
    #END DEF

    def show(self):
        """Shows the image the user is currently working on"""
        img_to_array = asarray(self.__as_array())
        Image.fromarray(img_to_array).show()
        del img_to_array
    #END DEF

    def reset(self):
        """Resets this object to the original image"""
        #The results of calling asarray() on the now created Image object is a 4-dimensional
        # array. The original array is made up of rows, each row is made up of pixels, and
        # each pixel is a set of 3 values (R,G,B of the pixel)
        tmpPixels = asarray(self.__myImage)
        self.pixels = []
        #Now we are going to mirror the structure of the return of asarray(), only each
        # pixels will now be an object
        rowCount = 0
        for row in tmpPixels:
            self.pixels.append([])
            colCount = 0
            for pixel in row:
                pixel = tuple([int(val) for val in list(pixel)])
                coord = (colCount, rowCount)
                self.pixels[-1].append( rgbPixel(pixel,coord) )
                colCount+=1
            #END FOR
            rowCount+=1
        #END FOR
    #END DEF

    def __as_array(self):
        """
        Converts the 3-dimensional array of pixel objects into a 4-dimensional
         array of RGB values (each pixel object is converted to an array)
        """
        tempArray = []
        for row in self.pixels:
            tempArray.append([])
            for pixel in row:
                init_arr = pixel._as_array()
                append_arr = [uint8(rgbVal) for rgbVal in init_arr]
                tempArray[-1].append(append_arr)
        #END FOR
        return tempArray
    #END DEF

    def __str__(self):
        """Returns a string representation of this object"""
        shortInput = self.inputFilename.split("/")[-1].split("\\")[-1]
        return ("RGB Image named {}\nSize is {}x{} pixels".format(shortInput, self.width, self.height)
                )
    #END DEF
#END CLASS
