"""This is a utility script intended to convert images to
particular pixel size for display in the portal"""

#!/usr/bin/python

from PIL import Image
import os, sys

path = "C:/Users/feroz/Documents/ecommerce/product_images"
dirs = os.listdir( path )

def resize():

    for item in dirs:
        print(item)
        print(path+item)
        print(os.path.isfile(path+"/"+item))
        if os.path.isfile(path+"/"+item):
            im = Image.open(path+"/"+item)
            print("print f")
            f, e = os.path.splitext(path+item)

            imResize = im.resize((340,340))
            imResize.save(f + ' resized.jpg', 'JPEG', quality=90)

resize()