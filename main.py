from pydoc import classname
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = '/Users/edirose/Desktop/drivers/chromedriver'
options = Options()

options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')

right_now = datetime.now()

options.headless = False
driver = webdriver.Chrome(chrome_driver, options=options)

try: 
    site = driver.get('https://www.strategyblocks.com/strategyblocks-full-manual/getting-started/basic-terminology/')
except:
    print('could not load driver')
finally:
    print(site)
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "post-content")))
    #image = element.screenshot('./',right_now,'.png')
    print(element)
    driver.close()

#height = driver.execute_script("return document.body.scrollHeight")
#options.add_argument("window-size=height, 2000")



##location = element.location
##size = element.size
##ss = driver.save_screenshot('test.png')

##left = location['x']
##top = location['y']
##right = location['x'] + size['width']
##bottom = location['y'] + size['height']