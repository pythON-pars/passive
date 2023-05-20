import pickle
from loguru import logger
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def save_cookeis(*, name, url):
    """
        This method will save cookies of various sites, even if it lies in this form for now, this is the most scourge version. 
    """
    driver = webdriver.Chrome('./chromedriver') # your web driver for chrome should be listed here https://chromedriver.chromium.org/downloads
    driver.get(url)

    driver.refresh()

    input('Save cookies: ')

    pickle.dump(driver.get_cookies(), open(f"./cookies/{name}","wb"))  

    return

def vk_task(urls="https://vk.com/gtr_nissan_top"):
    """
        This method logs in to VK which we will set for it, for some reason it rejects cookies, so we use normal authorization
    """

    logger.info("Start vk task")

    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome('./chromedriver', options=options)
    
    driver.get("https://vk.com")

    driver.implicitly_wait(10)
    try:
        if driver.find_element(By.CLASS_NAME, "narrow_column").find_element(By.TAG_NAME, "a"):
            print(driver.find_element(By.CLASS_NAME, "narrow_column").find_element(By.TAG_NAME, "a").text.strip())
    except:
        input_login = driver.find_element(By.XPATH, '//*[@id="index_email"]')
        input_login.send_keys('YOU_LOGIN')
        input_login.send_keys(Keys.ENTER)
        sleep(5)
        
        driver.implicitly_wait(5)
        input_password = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input')
        input_password.send_keys("YOU_PASSWORD")
        sleep(1) 
        input_password.send_keys(Keys.ENTER)        
    
    sleep(2)
    driver.get(urls)
    
    logger.info("Start vk forward in comuniti")
    try:
        driver.implicitly_wait(5)
        ####################### this line of code subscribes to publics or joins a community if it is a group #######################
        driver.find_element(By.CLASS_NAME, "PageCover__actions").find_elements(By.CLASS_NAME, "FlatButton")[-1].click()
        ##################################################################################################################################
    except:
        try:
            driver.implicitly_wait(5)
            driver.find_element(By.CLASS_NAME, "page_block").find_element(By.TAG_NAME, "button").click()
        except:
            logger.error('Error forward')
    
    sleep(5)

vk_task()
