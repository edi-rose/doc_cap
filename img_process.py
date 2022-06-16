from PIL import Image
from PIL import ImageFilter
import os
import glob
import pytesseract
import time
import clear
from PyPDF2 import PdfMerger


def getNames():
    files = list(filter(os.path.isfile, glob.glob('./images/'+"*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def to_pdf(name: str):
    img = Image.open(name)
    name_no_ext = name.replace(".png", "")
    im_pdf = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
    with open(name_no_ext+'.pdf', 'w+b') as f:
        f.write(im_pdf) 
        return f.read(im_pdf)

# def combine_pdfs():
#     names= getNames()
#     im_1 = Image.open(names[0])
#     im_list = []
#     for i,x in enumerate(names): 
#         if i != 0:
#             im_list.append(to_pdf(x))
#     im_1.save('./images/current_docs.pdf', save_all= True, append_images=im_list)

def combine_pdfs():
    names = getNames()
    merger = PdfMerger()
    for pdf in names: 

        merger.append(pdf)
    merger.write('docs_latest.pdf')
    merger.close()

#crops the sides of the screenshot, values for left right can be adjusted. 
def cropScreenshot(name):
    im = Image.open(name)
    left = im.width / 3.7
    right = im.width * 0.95
    box = (left, 0, right, im.height)
    im_crop = im.crop(box)
    im_crop.save(name, "PNG")
    return True

# uses image filter sharpen, TODO: test more filters
def sharpenImg(name):
    im = Image.open(name)
    im.filter(ImageFilter.SHARPEN).save(name)

# loops through page images, crops and sharpens each
def processImages():
    im_file_paths = getNames()
    for x in im_file_paths: 
        cropScreenshot(x)
        to_pdf(x)
        sharpenImg(x)
    clear.clear_pngs()
    combine_pdfs()
    clear.clear_pdfs()
    return