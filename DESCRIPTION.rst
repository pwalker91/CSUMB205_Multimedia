===========================================================
CSUMB's CST205 - A simple Image Class
===========================================================

This project offers students acces to a simple RGBImage class, which
is built on the use of the Image module in the PIL package. As PIL is no
longer updated for Python 3, this package relies on Pillow.



Python usage
===========================================================
The interface is very simple::
      #This is how you import the necessary class
    from SimpleImage.ImageClass import RGBImage

      #This is how you actually create an object
    myImage = RGBImage("/absolute/path/to/your/image")

      #NOTE: If you leave the constructor empty, tkinter will
      # open a file dialog, asking you to choose a file
    myImage = RGBImage("") ===>  tkinter filedialog GUI

      #Now that we have an image imported, what values do we have?
      #We can get the image's size, or number of pixels
    numOfPixels = myImage.size
      #We can also get the width and heigh individually
    myWidth = myImage.width
    myHeight = myImage.height

      #The most important part of our image, however, is the list of pixels
    a_pixel = myImage.pixels[0]
      #Each element of the images list "pixels" is an RGBPixel object. These
      # objects have a "red", "green", and "blue" attribute, which are integers.
      # We can then loop through every pixels and set it's blue or red values
    for pixel in myImage.pixels:
        pixel.setRed(255)
    #END FOR

      #If a pixel's attribute is set to anything above 255, the object will
      # automatically wrap the value around. For example, setting a pixel's
      # red value to 300 will actually set it to 300-256, or 44
    myImage.pixels[0].setRed(300) # ===> myImage.pixels[0] red is now 44



Contributors
===========================================================
* Peter Walker https://github.com/pwalker91


===========================================================
