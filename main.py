from curses import window
from json import load
from turtle import window_height
from matplotlib.backend_bases import LocationEvent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from PIL import ImageFilter

from io import BytesIO
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
        site = driver.get('https://www.strategyblocks.com/strategyblocks-full-manual/basic-navigation//')
    except:
        print('couldnt load site')
    finally:
        return site        

def main():
    driver = getDriver()
    loadPage(driver)
    post_body = getPostContent(driver)

    #removes the sidebar, header and footer
    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    
    num_of_screenshots = 0
    names = []
    while screenshotsHaveCoveredPost(driver, post_body, num_of_screenshots) is False:
        name_latest = createName(num_of_screenshots)
        takeScreenshot(post_body, name_latest)
        names.append(name_latest)
        num_of_screenshots = num_of_screenshots + 1
        print(driver.get_window_size()["height"]-20)
        driver.execute_script("window.scrollBy(0, "+str(driver.get_window_size()["height"])+")")

    processImages(names)
    driver.close()

    

def screenshotsHaveCoveredPost(driver, element, iteration):
    window_height = driver.get_window_size()['height']
    el_height = element.size['height']

    if el_height >(window_height * iteration):
        return False
    else: 
        return True

def createName(num):
    date_time = str(num)+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    name = './'+date_time+'.png'
    return name

def takeScreenshot(element, name):
    element.screenshot(name)

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

def sharpenImg(name):
    im = Image.open(name)
    im.filter(ImageFilter.SHARPEN).save(name)
    

def processImages(names):
    for x in names: 
        while not os.path.exists(x):
            time.sleep(1)
        if os.path.isfile(x):
            cropScreenshot(x)
            sharpenImg(x)
    return

main()