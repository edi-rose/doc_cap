from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus

import time
import os.path
import img_process 
import clear
import urllib as url

def getDriver(): 
    gecko_driver = '/Users/edirose/Desktop/drivers/geckodriver'
    options = Options()
    options.headless = True
    return webdriver.Firefox(executable_path=gecko_driver ,options=options)
    
def findCookieButton(driver):
    WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn")).click()
        )

# kicks off all processes for a single page.
def main(page):
    driver = getDriver()
    driver.set_window_position(0, 0)
    driver.set_window_size(1800, 800)
    driver.get(page['link'])
    post_body = getPostContent(driver)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element((By.CLASS_NAME, "cli-bar-message"))
    )

    #removes the sidebar, header and footer
    driver.execute_script("return document.getElementsByClassName('fusion-column-wrapper fusion-flex-column-wrapper-legacy')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-footer')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('fusion-header-wrapper')[0].remove();")
    driver.execute_script("return document.getElementsByClassName('to-top-container')[0].remove();")
    driver.execute_script("return document.getElementById('cookie-law-info-again').remove();")
    os.makedirs('./images/'+ page['parent'].replace(" ", "_"), exist_ok=True)
    name = './images/' + page['parent'].replace(" ", "_") + "/" + '/' +page['name'].replace(" ", "_")+'.png'
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

def getPages():
    driver = getDriver()
    # live site 
    driver.get("https://www.strategyblocks.com/strategyblocks-full-manual/")

    # staging site
    #driver.get('https://sbstagingphpup.wpengine.com/strategyblocks-full-manual/')
    
    pages=[]
    for x in driver.find_elements(by=By.CLASS_NAME, value='content-box-wrapper'):
        parent_name = x.find_element(by=By.CLASS_NAME, value='content-box-heading').text  
        link_container = x.find_element(by=By.CLASS_NAME, value='content-container')
        for a in link_container.find_elements(by=By.TAG_NAME, value='a'):
             pages.append({'name': a.text, 'link': a.get_attribute('href'), 'parent': parent_name})
    
    driver.close()
    return pages

def kickoff():
    clear.clear_pngs()
    clear.clear_pdfs()
    pages = getPages()

    for page in pages: 
        main(page)
    
    img_process.processImages()
    clear.clear_pngs()
    clear.clear_pdfs()
   
    print('doc capture complete')
    return

def getHeader():
    driver = getDriver()
    el = driver.find_element(by=By.TAG_NAME, value='h1')
    return el.text

#main({'link':'file:///Users/edirose/Desktop/StrategyBlocks%20Downloadable%20Guide%20Header%20Page%20-.html', 'name':'Header Image', 'parent':'../'})
kickoff()
#main('https://sbstagingphpup.wpengine.com/strategyblocks-full-manual/stadard-options-and-where-to-find-the-options-menu/')