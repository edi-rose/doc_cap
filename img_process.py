from PIL import Image
from PIL import ImageFilter
import os
import glob
import pytesseract
import time
import clear
from PyPDF2 import PdfMerger


def getNames(type: str):
    files = list(filter(os.path.isfile, glob.glob('./images/**/*'+type, recursive=True)))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def toPDF(name: str):
    img = Image.open(name)
    name_no_ext = name.replace(".png", "")
    im_pdf = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
    with open(name_no_ext+'.pdf', 'w+b') as f:
        f.write(im_pdf) 

def combinePDFs():
    names = getNames('pdf')
    merger = PdfMerger()
    merger.append('./Header_Image.pdf', 'Introduction')
    for pdf_path in names: 
        bookmark = os.path.basename(os.path.normpath(pdf_path))[:-4].replace('_', ' ')
        merger.append(pdf_path, bookmark)
    merger.write('docs_latest.pdf')
    merger.close()

#crops the sides of the screenshot, values for left right can be adjusted. 
def cropScreenshot(name):
    im = Image.open(name)
    left = im.width / 3.8
    right = im.width * 0.95
    box = (left, 0, right, im.height)
    im_crop = im.crop(box)
    im_crop.save(name, "PNG")
    return True

# uses image filter sharpen, TODO: test more filters
def sharpenImg(name):
    im = Image.open(name)
    im.filter(ImageFilter.SHARPEN).save(name)
    return

# loops through page images, crops and sharpens each
def processImages():
    im_file_paths = getNames('png')
    for x in im_file_paths: 
        cropScreenshot(x)
        sharpenImg(x)
        toPDF(x)
    combinePDFs()
    return