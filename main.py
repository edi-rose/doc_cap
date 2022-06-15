from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from PIL import ImageFilter
import time
import os.path

def getDriver(): 
    gecko_driver = '/Users/edirose/Desktop/drivers/geckodriver'
    options = Options()
    #options.headless = False
    return webdriver.Firefox(executable_path=gecko_driver ,options=options)
    
# kicks off all processes for a single page.
def main(link):
    driver = getDriver()
    driver.get(link)
    post_body = getPostContent(driver)

    #removes the sidebar, header and footer
    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('to-top-container')[0].remove();")
    name = './images/'+ driver.find_element_by_tag_name('h1').text.replace(" ", "")+'.png'
    takeScreenshot(post_body, name)
    processImage(name)
    driver.close()

#creates dynamic filenames for our images C
def createName():
    date_time = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    name = './images/'+date_time+'.png'
    return name

def takeScreenshot(element, name):
    element.screenshot(name)

# waits until the body is loaded (side bar included)
def getPostContent(driver):
    post_body = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "post-content"))
    )
    return post_body

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
def processImage(name):
    while not os.path.exists(name):
        time.sleep(1)
    if os.path.isfile(name):
        cropScreenshot(name)
        sharpenImg(name)
    return

def getLinks():
    driver = getDriver()
    driver.get("https://www.strategyblocks.com/strategyblocks-full-manual/")

    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    link_list = []

    #bit of a hack to exclude other links not suitable for documentation capture
    banned_links = [None, '', 'https://www.strategyblocks.com/strategyblocks-full-manual/#', 'https://www.strategyblocks.com/strategyblocks-full-manual/#content', 'https://www.strategyblocks.com/blog/author/carolinepurre/']

    for x in driver.find_elements_by_tag_name('a'):
        link = x.get_attribute('href')
        if link not in banned_links and link not in link_list:
            link_list.append(x.get_attribute('href'))
    driver.close()
    return link_list

def kickoff():
    links = getLinks()
    print(links)

    for link in links: 
        main(link)
    return

def getHeader():
    driver = getDriver()
    el = driver.find_element_by_tag_name('h1')
    return el.text

kickoff()

