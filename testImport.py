from Image import RGBImage
x = RGBImage("/Users/peterwalker/Desktop/test.png")
print(len(x.myPixels))
for t in range(500):
    print(str(x.myPixels[t]))
