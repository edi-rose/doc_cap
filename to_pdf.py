from PIL import Image
from PIL import ImageFilter
import os
import glob

from numpy import save 

def getNames():
    files = list(filter(os.path.isfile, glob.glob('./images/'+"*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def getImages():
    file_names= getNames()
    images = []
    for name in file_names: 
        img = Image.open(name)
        im_pdf = img.convert('RGB')
        images.append(im_pdf)
    return images

def saveList():
    images= getImages()
    im_1 = images[0]
    im_list = []
    for i,x in enumerate(images): 
        if i != 0:
            im_list.append(x)
    im_1.save('./images/current_docs.pdf', save_all= True, append_images=im_list)

saveList()