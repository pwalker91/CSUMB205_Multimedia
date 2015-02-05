from SimpleImage.ImageClass import RGBImage

x = RGBImage("/a/path/to/an/image.png")
print(len(x.myPixels))
for t in range(20):
    print(str(x.myPixels[t]))
