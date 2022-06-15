from PIL import Image
from PIL import ImageFilter
import os



def getNames():
    file_names = []
    for file in os.listdir('./images/'):
        if file.endswith('.png'):
            file_names.append(file)
    return file_names

def getImages():
    file_names= getNames()
    images = []
    for name in file_names: 
        img = Image.open('./images/'+name)
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

