#!/usr/local/bin/python3
"""
-------------------------------------------------------------------------------
SIMPLE IMAGE.PY

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
from platform import system
import os
#import sys
#import subprocess
from numpy import asarray, uint8
from tkinter.filedialog import (askdirectory, askopenfilename)
from PIL import Image
#END IMPORTS




class rgbPixel(object):

    """
    A simple class for accessing attributes of an RGB Pixel

    ATTRIBUTES:
        red     An integer between 0 and 255.
                 Accessible by getRed() and setRed()
        blue    An integer between 0 and 255.
                 Accessible by getBlue() and setBlue()
        green   An integer between 0 and 255.
                 Accessible by getGreen() and setGreen()
        X       An integer, representing the pixel's location in a picture.
                 Accesible with getX()
        Y       An integer, representing the pixel's location in a picture.
                 Accesible with getY()
    """

    # CLASS ATTRIBUTES -----------
    __red = 0
    __green = 0
    __blue = 0
    __x=0
    __y=0
    # ----------------------------


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
        #The return of setColor() is True if args[0] is a list or tuple
        if self.setColor(*args):
            args = args[1:]
        else:
            args = args[3:]
        #END IF/ELSE
        self.__setCoord(*args)
    #END DEF


    # CLASS SPECIFIC DECORATORS and VALUE CHECKERS -----------------------------

    def __checkVal(func):
        """
        A decorator that will make sure that the color arguments passed are viable.
        The arguments we are expected are "self", and an integer value between
         0 and 255.
        """
        def wrapper(*args, **kwargs):
            if not isinstance(args[1], (int,float)):
                raise ValueError("You must pass in a number value. Was passed {}".format(repr(args[1])))
            #Casting args to a list so that we can modify the values (args was originally
            # a tuple, which is immutable)
            args = list(args)
            args[1] = int(args[1])
            #This will make sure that the value is between 0 and 255, by iteratively
            # adding or subtracting 256
            while args[1] > 255 or args[1] < 0:
                if args[1] < 0:
                    args[1] += 256
                elif args[1] > 255:
                    args[1] -= 256
            #END WHILE
            #Casting args back to being a tuple
            args = tuple(args)
            return func(*args, **kwargs)
        return wrapper
    #END DEF

    def __checkCoord(func):
        """
        A decorator that will make sure that the coordinate arguments passed are viable.
        The arguments we are expected are "self", and an integer value greater than 0.
        """
        def wrapper(*args, **kwargs):
            if not isinstance(args[1], (int,float)):
                raise ValueError("You must pass in a number value. Was passed {}".format(repr(args[1])))
            #Checking for negative coordinate
            if args[1]<0:
                raise ValueError("You must pass in a POSITIVE number value. "+
                                 "Was passed {}".format(repr(args[1])))
            #Casting args to a list so that we can modify the values (args was originally
            # a tuple, which is immutable)
            args = list(args)
            args[1] = float(args[1])
            #Casting args back to being a tuple
            args = tuple(args)
            return func(*args, **kwargs)
        return wrapper
    #END DEF

    def __sameObject(func):
        def wrapper(*args, **kwargs):
            if not isinstance(args[1], args[0].__class__):
                raise TypeError("You must compare objects of the same type. Cannot compare "+
                                "{0} and {1}".format(args[0].__class__, args[1].__class__))
            return func(*args, **kwargs)
        return wrapper
    #END DEF

    def __isPixel(self, pixel):
        """Simple function to make sure that the passed object is a pixel"""
        if not isinstance(pixel, self.__class__):
            raise ValueError("You must give an rgbPixel object to 'pixel'")
        return True
    #END DEF

    def __isColor(self, color):
        """Simple function to make sure that the passed color has 3 integers"""
        if not isinstance(color, (tuple,list)) and len(color) != 3:
            raise ValueError("You must give an RGB value as a tuple (r,g,b) to 'color'")
        if not all( [isinstance(val, int) for val in list(color)] ):
            raise ValueError("You must give three RGB values as integers to the keyword arg 'color'")
        return True
    #END DEF


    # GETTERS AND SETTERS ------------------------------------------------------

    #Color setting functions
    @__checkVal
    def setRed(self, val):
        """Sets the RED values to given number"""
        self.__red = val
    def getRed(self):
        """Gets the RED value of the picture"""
        return self.__red

    @__checkVal
    def setGreen(self, val):
        """Sets the GREEN values to given number"""
        self.__green = val
    def getGreen(self):
        """Gets the GREEN value of the picture"""
        return self.__green

    @__checkVal
    def setBlue(self, val):
        """Sets the BLUE values to given number"""
        self.__blue = val
    def getBlue(self):
        """Gets the BLUE value of the picture"""
        return self.__blue

    #Coordinate setting functions
    @__checkCoord
    def __setX(self, coord):
        self.__x = coord
    def getX(self):
        """Gets the X-coordinate of this pixel in the picture"""
        return self.__x

    @__checkCoord
    def __setY(self, coord):
        self.__y = coord
    def getY(self):
        """Gets the Y-coordinate of this pixel in the picture"""
        return self.__y

    #Setters and Getters for multiple attributes
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
        if len(args) == 0:
            raise ValueError("You must pass in 2 NUMBER values (as a tuple or separately). "+
                             "You passed in {}".format(len(args)))
        if not isinstance(args[0], (list,tuple)):
            color = list(args[:3])
            _usingList = False
        else:
            color = list(args[0][:3])
            _usingList = True
        if len(color)!=3:
            raise ValueError("You must pass in 3 NUMBER values (as a tuple or separately). "+
                             "You passed in {}".format(len(color)))
        self.setRed(color[0])
        self.setGreen(color[1])
        self.setBlue(color[2])
        return _usingList
    #END DEF

    def getColor(self):
        """Gets all 3 RGB values of this picture as a tuple"""
        return self._color_as_tuple()

    def __setCoord(self, *args):
        """
        Sets this pixel's X and Y coordinate to the given values
        ARGS:
            (x,y)   Tuple/List of the pixel's X and Y coordinate
                or
            x       The X-part of the this pixel's location within the picture
            y       The Y-part of the this pixel's location within the picture
        """
        if len(args) == 0:
            raise ValueError("You must pass in 2 NUMBER values (as a tuple or separately). "+
                             "You passed in {}".format(len(args)))
        if not isinstance(args[0], (list,tuple)):
            coord = list(args[:2])
            _usingList = False
        else:
            coord = list(args[0][:2])
            _usingList = True
        if len(coord)!=2:
            raise ValueError("You must pass in 2 NUMBER values (as a tuple or separately). "+
                             "You passed in {}".format(len(coord)))
        self.__setX(coord[0])
        self.__setY(coord[1])
        return _usingList
    #END DEF

    def getCoord(self):
        """Gets the X and Y coordinate of this pixel as a tuple"""
        return self._coord_as_tuple()


    # CONVERTERS ---------------------------------------------------------------

    def _color_as_array(self):
        """Returns the pixel's RGB values in a list format"""
        return [self.__red, self.__green, self.__blue]

    def _color_as_tuple(self):
        """Returns the pixel's RGB values in a tuple format"""
        return (self.__red, self.__green, self.__blue)

    def _coord_as_array(self):
        """Returns the pixel's RGB values in a list format"""
        return [self.__x, self.__y]

    def _coord_as_tuple(self):
        """Returns the pixel's RGB values in a tuple format"""
        return (self.__x, self.__y)


    # FUN PIXEL MATH FUNCTIONS -------------------------------------------------

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
            self.__isColor(kwargs['color'])
        elif "pixel" in kwargs:
            self.__isPixel(kwargs['pixel'])
        #END IF/ELIF
        if "color" in kwargs:
            givenR, givenG, givenB = kwargs['color']
        elif "pixel" in kwargs:
            givenR, givenG, givenB = kwargs['pixel']._color_as_tuple()
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
        self.__isPixel(pixel)
        xDist = pixel.getX()-self.getX()
        yDist = pixel.getY()-self.getY()
        from math import sqrt
        return sqrt(xDist**2 + yDist**2)
    #END DEF

    def _avgValue(self):
        return int((self.__red + self.__green + self.__blue)/3)
    #END DEF


    # STRING FUNCTIONS ---------------------------------------------------------

    def __str__(self):
        """Returns a string representation of this object"""
        return ("Pixel at ({},{}): ".format(self.__x, self.__y)+
                "RED={}, GREEN={}, BLUE={}".format(self.__red, self.__green, self.__blue))
    #END DEF


    # COMPARATORS --------------------------------------------------------------

    @__sameObject
    def __lt__(self, other):
        """Less than comparison, based on average pixel value"""
        if self._avgValue() < other._avgValue():
            return True
        return False
    #END DEF
    @__sameObject
    def __eq__(self, other):
        """Equal comparison, based on average pixel value"""
        if self._avgValue() == other._avgValue():
            return True
        return False
    #END DEF

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    def __le__(self, other):
        return self.__eq__(other) or self.__le__(other)
#END CLASS ---------------------------------------------------------------------






class rgbImage(object):

    """
    A simple class for accessing attributes of an RGB Pixel

    ATTRIBUTES:
        inputFilename   String, the absolute path of the file used for input.
                         Empty if blank image was created
        outputFilename  String, the absolute path where the image will be saved.
                         Empty if blank image was created
        pixels          List, a 2-dimensional array of rgbPixel objects
        height          Integer, the height of the picture in pixels
        width           Integer, the width of the pixture in pixels
    """

    # CLASS ATTRIBUTES -----------
    inputFilename = ""
    outputFilename = ""

    __myImage = None
    __blank = False
    pixels = []

    height = 0
    width = 0
    # ----------------------------


    def __init__(self, inputFilename="", outputFilename="", blank=False, width=100, height=100):
        """
        Object initialization
        ARGS:
            self            this Object
            inputFilename   String, the location of the picture
            outputFilename  String, the location that this picture will be saved to
            blank           Boolean, whether this image should be a blank image
                width       Integer, the width of the blank image
                height      Integer, the height of the blank image
        """
        self.__blank = blank
        if not self.__blank:
            if not inputFilename:
                self.inputFilename = askopenfilename(initialdir=os.path.expanduser("~"),
                                                     title="Select the IMAGE FILE",
                                                     filetypes=[('JPG Image', '.jpg'),
                                                                ('JPEG Image', '.jpeg'),
                                                                ('GIF Image', '.gif'),
                                                                ('PNG Image', '.png')
                                                                ],
                                                     multiple=False
                                                     )
                if not self.inputFilename:
                    raise ValueError("You must choose a file for this class to work.")
                self.inputFilename = os.path.abspath(self.inputFilename)
            else:
                self.inputFilename = os.path.abspath(inputFilename)
                if system()!="Windows":
                    self.inputFilename = self.inputFilename.replace("\\","").strip()
                acceptedExt = ["jpg","jpeg","png","gif"]
                if not os.path.isfile(self.inputFilename) or \
                        self.inputFilename.split(".")[-1].lower() not in acceptedExt:
                    raise ValueError("You must pass in a legitimate picture file. "+
                                     "Use one of the following options:"+str(acceptedExt))
            #END IF/ELSE
            if not outputFilename:
                dirname = os.path.dirname(self.inputFilename)
                filename = os.path.basename(self.inputFilename)
                filename = filename.split(".")[0]+"_altered."+filename.split(".")[1]
                self.outputFilename = os.path.join(dirname, filename)
            else:
                self.outputFilename = os.path.abspath(outputFilename)
            #END IF/ELSE
            if os.path.isfile(self.outputFilename):
                print("{} will be overwritten if this image is saved. ".format(os.path.basename(self.outputFilename))+
                      "Consider saving to another location."
                      )
            #END IF
            print("Importing image {}".format(self.inputFilename))
        else:
            self.width, self.height = width, height
            print("Creating Blank Image, {}x{}".format(self.width, self.height))
        #END IF/ELSE

        #Calls self.reset(), as the reset function does what we want to do initially
        self.reset()
    #END DEF


    # CLASS SPECIFIC DECORATORS and CHECKERS -----------------------------------

    def __checkCoordPair(func):
        def coord_wrapper(*args, **kwargs):
            def checkPoint(val, maxVal):
                if val<0 or val>maxVal:
                    return False
                return True
            #END DEF

            if isinstance(args[1], (tuple,list)):
                if len(args[1])!=2:
                    raise ValueError("You must pass in two values as a coordinate. "+
                                     "Was passed {}".format(repr(args[1]))
                                     )
                if not all([isinstance(coord, int) for coord in args[1]]):
                    raise ValueError("You must pass in two integers for coordinates. "+
                                     "Was passed {}".format(repr(args[1]))
                                     )
                x,y = tuple(args[1])
                if not checkPoint(x, args[0].width-1) and not checkPoint(y, args[0].height-1):
                    raise ValueError("You must pass in POSITIVE integers. "+
                                     "Was passed {}".format(repr([x,y]))
                                     )
            else:
                if not all( [isinstance(elem,int) for elem in [args[1],args[2]]] ):
                    raise ValueError("You must pass in integer value. "+
                                     "Was passed {}".format(repr([args[1],args[2]]))
                                     )
                x = args[1]
                y = args[2]
                if not checkPoint(x, args[0].width-1) and not checkPoint(y, args[0].height-1):
                    raise ValueError("You must pass in POSITIVE integers. "+
                                     "Was passed {}".format(repr([x,y]))
                                     )
            #END IF/ELSE
            return func(*args, **kwargs)
        return coord_wrapper
    #END DEF


    # GETTERS ------------------------------------------------------------------

    @__checkCoordPair
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
        if isinstance(args[0], (tuple, list)):
            x,y = args[0]
        else:
            x = args[0]
            y = args[1]
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

    def setName(self, name):
        """
        Given a new name (as a String), sets the output filename
        ARGS:
            name    String, the new name of the to-be-saved file
        RETURNS:
            Boolean, True if file does not exist, False otherwise
        RAISES:
            Value Error if name is not string
        """
        if not isinstance(name, str):
            raise ValueError("You must pass in a string for your new image name")
        if self.__blank and not self.outputFilename:
            print("Please choose the directory you will want the file saved in...")
            outputPath = askdirectory(initialdir=os.path.expanduser("~"),
                                      title="Select the FOLDER to contain the image",
                                      mustexist=True)
            name = os.path.splitext(name)[0]+".png"
            self.outputFilename = os.path.abspath(os.path.join(outputPath, name))
        elif not self.outputFilename:
            dirname = os.path.dirname(self.inputFilename)
            name = name+"."+os.path.splitext(self.inputFilename)[1]
            self.outputFilename = os.path.abspath(os.path.join(dirname, name))
        else:
            dirname = os.path.dirname(self.outputFilename)
            name = name+"."+os.path.splitext(self.outputFilename)[1]
            self.outputFilename = os.path.abspath(os.path.join(dirname, name))
        #END IF/ELSE
        if os.path.isfile(self.outputFilename):
            print("{} will be overwritten if this image is saved. ".format(os.path.basename(self.outputFilename))+
                  "Consider saving to another location."
                  )
            return False
        #END IF
        return True
    #END DEF

    def save(self, filename="", forceOverwrite=False):
        """
        This will save the current object to a specified location
        ARGS:
            self            this Object
            filename        OPTIONAL. String, the name or location to be saved to.
            forceOverwrite  OPTIONAL. Boolean, whether to force overwrite of file
                             at location 'filename' or 'self.outputFilename'
        RETURNS:
            none
        RAISES:
            none.
            Will ask user if they wish to overwrite a file if it exists at the given
             location in filename, or at self.outputFilename
        """
        if not self.outputFilename:
            print("Please choose the directory you will want the file saved in...")
            outputPath = askdirectory(initialdir=os.path.expanduser("~"),
                                      title="Select the FOLDER to contain the image",
                                      mustexist=True)
            name = "simpleImage_output.jpg"
            self.outputFilename = os.path.abspath(os.path.join(outputPath, name))
        if filename:
            self.setName(filename)
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
    #END DEF

    def reset(self):
        """Resets this object to the original image"""
        #We need to open the file to get the data from it. If self.__blank is not
        # true, then we need to create a new image.
        if not self.__blank:
            self.__myImage = Image.open(self.inputFilename)
        else:
            self.__myImage = Image.new("RGB", (self.width, self.height))
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

        #Setting some other useful variables for users
        self.width, self.height = self.__myImage.size

        #Closing the file that we've opened
        self.__myImage.close()
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
                init_arr = pixel._color_as_array()
                append_arr = [uint8(rgbVal) for rgbVal in init_arr]
                tempArray[-1].append(append_arr)
        #END FOR
        return tempArray
    #END DEF

    def __str__(self):
        """Returns a string representation of this object"""
        shortInput = os.path.basename(self.inputFilename)
        return ("RGB Image named {}\nSize is {}x{} pixels".format(shortInput, self.width, self.height)
                )
    #END DEF
#END CLASS ---------------------------------------------------------------------
