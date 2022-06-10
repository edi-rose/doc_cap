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

def getDriver(): 
    chrome_driver = '/Users/edirose/Desktop/drivers/chromedriver'
    options = Options()
    options.headless = False
    return webdriver.Chrome(chrome_driver, options=options)

#this will need to be updated once we have a method and want to automate every page
def loadPage(driver):
    try: 
        site = driver.get('https://www.strategyblocks.com/strategyblocks-full-manual/getting-started/basic-terminology/')
    except:
        print('couldnt load site')
    finally:
        return site        

def main():
    driver = getDriver()
    loadPage(driver)
    post_body = getPostContent(driver)
    nav_top = getNavTop(driver)
    # we want to scroll down to the top of the post minus the height of the floating nav
    first_scroll_height = post_body.location['y'] - nav_top.size['height']
    
    driver.execute_script("window.scrollTo(0, "+str(first_scroll_height)+")")
    num_of_screenshots = 0
    while screenShotsHaveCoveredPost(driver, post_body, num_of_screenshots, first_scroll_height) is False:
        takeScreenshot(post_body, num_of_screenshots)
        num_of_screenshots = num_of_screenshots + 1
        driver.execute_script("window.scrollBy(0, "+str(driver.get_window_size()["height"] - first_scroll_height)+")")

    driver.close()

def screenShotsHaveCoveredPost(driver, element, iteration, first_scroll_height):
    window_height = driver.get_window_size()['height']
    el_height = element.size['height']

    if el_height > first_scroll_height + (window_height * iteration):
        print('False')
        return False
    else: 
        print('true')
        return True



def takeScreenshot(element, num):
    date_time = str(num)+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    name = './'+date_time+'.png'
    element.screenshot(name)

def getPostContent(driver):
    post_body = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "post-content"))
    )
    return post_body

def getNavTop(driver):
    nav_top = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fusion-secondary-main-menu"))
    )
    return nav_top

main()