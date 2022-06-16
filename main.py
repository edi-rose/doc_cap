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
import img_process 
import clear

def getDriver(): 
    gecko_driver = '/Users/edirose/Desktop/drivers/geckodriver'
    options = Options()
    options.headless = True
    return webdriver.Firefox(executable_path=gecko_driver ,options=options)
    
# kicks off all processes for a single page.
def main(link):
    driver = getDriver()
    driver.set_window_position(0, 0)
    driver.set_window_size(1800, 800)
    driver.get(link)
    post_body = getPostContent(driver)

    #removes the sidebar, header and footer
    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('to-top-container')[0].remove();")
    name = './images/'+ driver.find_element(by=By.TAG_NAME, value='h1').text.replace(" ", "").replace("/", '_')+'.png'
    takeScreenshot(post_body, name)
    driver.close()

#creates dynamic filenames for our images Currently Redundant
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

def getLinks():
    driver = getDriver()
    # live site 
    driver.get("https://www.strategyblocks.com/strategyblocks-full-manual/")

    # staging site
    #driver.get('https://sbstagingphpup.wpengine.com/strategyblocks-full-manual/')

    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    link_list = []

    #bit of a hack to exclude other links not suitable for documentation capture
    # considering adding News, Calendar Integration
    banned_links = [None, '', 'https://www.strategyblocks.com/strategyblocks-full-manual/#', 'https://www.strategyblocks.com/strategyblocks-full-manual/#content', 'https://www.strategyblocks.com/blog/author/carolinepurre/']

    for x in driver.find_elements(by=By.TAG_NAME, value='a'):
        link = x.get_attribute('href')
        if link not in banned_links and link not in link_list:
            link_list.append(x.get_attribute('href'))
    driver.close()
    return link_list

def kickoff():
    links = getLinks()

    for link in links: 
        main(link)
    
    img_process.processImages()
    clear.clear_pngs()
    print('doc capture complete')
    return

def getHeader():
    driver = getDriver()
    el = driver.find_element(by=By.TAG_NAME, value='h1')
    return el.text

kickoff()
#main('https://sbstagingphpup.wpengine.com/strategyblocks-full-manual/stadard-options-and-where-to-find-the-options-menu/')