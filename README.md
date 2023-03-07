# Documentation-Capture
Small project to automatically generate a PDF version of our strategyblocks documentation.

# Requirements / Set up 
Bot requires the user to download the latest geckodriver and to update the method getDriver with the path to the driver. 
Bot requires python3 and has only been tested on MacOs
Img processing requires PyPDF2 and Tesseract/PyTesseract

# Current State
Bot currently can produce a PDF containing all the documentation on the live site.
Bot is dynamic and will update automatically when new pages are added / removed.
This is based on the links available on the main menu of the documentation. 
Bot uses PyTesseract to make screenshots selectable.

# Next Steps
It should be possible to do this by recreating pdfs based on the html and not with screenshots, this would produce a cleaner image. 
   
# How to run: 
Python3.9 main.py will create a new docs_latest.pdf 
Note Header_Image is created seperately from this process, any image you place with that name will be the first image in the output pdf. 