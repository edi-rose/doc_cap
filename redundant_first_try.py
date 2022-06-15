from random import randint
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
    
# kicks off all processes for a single page.
def main(link):
    driver = getDriver()
    print(link)
    driver.get(link)
    post_body = getPostContent(driver)

    #removes the sidebar, header and footer
    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('to-top-container')[0].remove();")

    #gets the view height, this is the height we care about when scrolling
    view_height = driver.execute_script("return window.visualViewport['height']")

    num_of_screenshots = 0
    names = []

    element_height = post_body.size['height']
    non_overlap = getScreenshotNonOverlap(element_height, view_height)
  
    while screenshotsHaveCoveredPost(element_height, num_of_screenshots, view_height) is False:
        name_latest = createName(num_of_screenshots)
        takeScreenshot(post_body, name_latest)
        names.append(name_latest)
        num_of_screenshots = num_of_screenshots + 1
        driver.execute_script("window.scrollBy(0, "+str(view_height)+")")

    processImages(names, non_overlap)
    driver.close()

# determines if we need to do more screenshots 
def screenshotsHaveCoveredPost(el_height, iteration, view_height):
    if el_height >(view_height * iteration):
        return False
    else: 
        print('true')
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
def mergeImages(names, non_overlap):
    im1 = Image.open(names[0])

   #here is the source of bug :) we need to be more precise with ss height  
    dst = Image.new('RGB', (im1.width, im1.height * (len(names) -1)+ non_overlap))
    count = 0
    for x in names: 
        x_img = Image.open(x)
        if count == 0:
            dst.paste(x_img, (0, 0))
        elif count == len(names) -1 and non_overlap != 0:
            width, height = x_img.size
            prev_img = Image.open(names[count-1])
            box = (0, height - non_overlap, width, height)
            new_img = x_img.crop(box)
            dst.paste(new_img, (0, prev_img.height))
        else: 
            prev_img = Image.open(names[count-1])
            dst.paste(x_img, (0, prev_img.height))
        count = count + 1
    name = createName(randint(1,100))
    dst.save(name)
    return



# loops through page images, crops and sharpens each
def processImages(names, overlap):
    for x in names: 
        while not os.path.exists(x):
            time.sleep(1)
        if os.path.isfile(x):
            cropScreenshot(x)
            sharpenImg(x)
    if len(names)>1:
        mergeImages(names, overlap)
    #for x in names: 
        #os.remove(x)
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

def getScreenshotNonOverlap(el_height, view_height):
    if el_height/view_height < 1: 
        return 0
    else: 
        return el_height % view_height

#main('https://www.strategyblocks.com/strategyblocks-full-manual/9-admin-functions/risk-management/')
#main('https://sbstagingphpup.wpengine.com/strategyblocks-full-manual/9-admin-functions/risk-management/')
#main('https://www.strategyblocks.com/strategyblocks-full-manual/monitor-metrics-risks-documents/metrics-table/')

main('https://sbstagingphpup.wpengine.com/strategyblocks-full-manual/stadard-options-and-where-to-find-the-options-menu/')

#kickoff()