from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from PIL import ImageFilter
import time
import os.path

def getDriver(): 
    chrome_driver = '/Users/edirose/Desktop/drivers/chromedriver'
    options = Options()
    options.headless = False
    return webdriver.Chrome(chrome_driver, options=options)

#this will need to be updated once we have a method and want to automate every page
def loadPage(driver):
    try: 
        site = driver.get('https://sbstagingphpup.wpengine.com/block-faces/')
    except:
        print('couldnt load site')
    finally:
        return site        

# kicks off all processes for a single page.
def main():
    driver = getDriver()
    loadPage(driver)
    post_body = getPostContent(driver)

    #removes the sidebar, header and footer
    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")

    #gets the view height, this is the height we care about when scrolling
    view_height = driver.execute_script("return window.visualViewport['height']")
    num_of_screenshots = 0
    names = []
    while screenshotsHaveCoveredPost(driver, post_body, num_of_screenshots) is False:
        name_latest = createName(num_of_screenshots)
        takeScreenshot(post_body, name_latest)
        names.append(name_latest)
        num_of_screenshots = num_of_screenshots + 1
        driver.execute_script("window.scrollBy(0, "+str(view_height)+")")

    processImages(names)
    driver.close()

# determines if we need to do more screenshots 
def screenshotsHaveCoveredPost(driver, element, iteration):
    window_height = driver.get_window_size()['height']
    el_height = element.size['height']

    if el_height >(window_height * iteration):
        return False
    else: 
        return True

#creates dynamic filenames for our images
def createName(num):
    date_time = str(num)+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    name = './'+date_time+'.png'
    return name

def takeScreenshot(element, name):
    element.screenshot(name)

# waits until the body is loaded (side bar included)
def getPostContent(driver):
    post_body = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "post-content"))
    )
    return post_body

#crops the left 25% of the image
def cropScreenshot(name):
    im = Image.open(name)
    left = im.width / 4
    box = (left, 0, im.width, im.height)
    im_crop = im.crop(box)
    im_crop.save(name, "PNG")
    return True

# uses image filter sharpen, TODO: test more filters
def sharpenImg(name):
    im = Image.open(name)
    im.filter(ImageFilter.SHARPEN).save(name)

# merges the images of a page vertically - loop count should be refactored
def mergeImages(names):
    im1 = Image.open(names[0])
    dst = Image.new('RGB', (im1.width, im1.height * len(names)))
    count = 0
    for x in names: 
        print(x)
        x_img = Image.open(x)
        if count == 0:
            dst.paste(x_img, (0, 0))
        else: 
            prev_img = Image.open(names[count-1])
            dst.paste(x_img, (0, prev_img.height))
        count = count + 1
    dst.save('./merged.png')
    return

# loops through page images, crops and sharpens each
def processImages(names):
    for x in names: 
        while not os.path.exists(x):
            time.sleep(1)
        if os.path.isfile(x):
            cropScreenshot(x)
            sharpenImg(x)
    if len(names)>1:
        mergeImages(names)
    return

#main()