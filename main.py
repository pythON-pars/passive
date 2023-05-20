import pickle
import random
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from fake_useragent import UserAgent
from taski import Task
import pdb
from loguru import logger

class Vktarget:
    def __init__(self):
        logger.info("Start")    
        self.urls = "https://vktarget.ru/list/"

        self.options = webdriver.ChromeOptions()
        self.options.headless = True 

        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument(f"user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.838 Yowser/2.5 Safari/537.36")

        # I sometimes used these lines to proxy my actions via the web
        # proxy = '127.0.0.1:9000' 
        # self.options.add_argument('--proxy-server=socks5://' + proxy)

        self.driver = webdriver.Chrome('./chromedriver', options=self.options)
        self.driver.get(self.urls)
        self.task = Task

    def vktarget(self):
        """
            A function that will listen to vktarget.ru and make 
            a decision based on what it listened to, a class will probably be implemented in the near future. Because it's easier!
        """

        sleep(2)
        for cookie in pickle.load(open("./cookies/update.pkl","rb")):
            self.driver.add_cookie(cookie)
        
        logger.info("add cookie")

        self.driver.refresh()

        sleep(2)
        self.driver.implicitly_wait(5)
        
        with open('test.html', 'w') as file:
            file.write(self.driver.page_source)

        # we enter from an infinite loop and send data for processing after a certain time, 
        # but you can do it randomly and through the appropriate library
        count_time = 1

        logger.info("Wait")

        # second_timeout is needed here so that the timer works correctly for us, this variable 
        # takes an integer value from the loop from the function that gives a random value in the range 
        second_timeout = 2
        while True:
            count_time += 1
            sleep(1)
            if count_time == int(second_timeout/2):
                logger.info(f'wait {second_timeout} / {count_time}')

            if count_time == second_timeout:

                self.driver.refresh()
                sleep(2)    
                # check the domain, if there are back ones, we execute, if not, then we return
                second_timeout = random.randint(100, 150)
                logger.info("chek domain info")
                self.chek_domain(self.driver.page_source)
                
                count_time = 0

                self.finish()
            
            # at the first error, that is, when the script crashes, it's worth checking how the 
            # authorization works, because cookies are changeable, so you need to think about the implementation of the login
            # to the portal, i.e. through an exception

    def chek_domain(self, page_html):
        """
            A function for checking a domain name, then in the loop there will already be a 
            selection by domain into the corresponding function 
        """
        
        soup = BeautifulSoup(page_html, 'lxml')
        try:
            bais_task = soup.find('div', {'class':'tabs__content-container full-width'}).find_all('div', {'class':'mdl-grid available__row bb-grey-1 pa-0'})
        except Exception as ex:
            logger.error("Old cookies, need plase update!")
        
        c = 0
        for i in bais_task:
            try:
                title_task = i.find('span').text
                task_url = i.find('a', {'class':'blue--text underline'}).get('href').split('/')[2]

                logger.debug(f"{title_task} || {task_url}")
            except:
                continue

            if i.find('button').text.strip() != "ПРОВЕРЕНО":
                self.driver.implicitly_wait(10)
                href_task = i.find('a', {'class':'blue--text underline'}).get('href')
                
                # the condition checks if the task is completed or not, so as not to execute what has already been completed :)
                if task_url == "vk.com":
                    try:
                        logger.info("VK TASK")
                        self.driver.find_element(By.CLASS_NAME, "available__table-container").find_elements(By.TAG_NAME, "a")[c].click()
                    except:
                        logger.warning("There was no assignment")
                        continue
                        
                    # switch to the window to complete the task, after it is completed, exit this tab (close) and wait for verification
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    
                    self.task.vk_task(self=self, urls=href_task, title_tasks=title_task)

                    self.driver.switch_to.window(self.driver.window_handles[0])
                    sleep(1.5)
                    
                if task_url[-9:] == "quora.com":
                    try:
                        logger.info('quora TASK')
                        self.driver.implicitly_wait(5)
                        self.driver.find_element(By.CLASS_NAME, "available__table-container").find_elements(By.TAG_NAME, "a")[c].click()
                    except:
                        logger.warning("Не было задания")
                        continue
                
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self.task.quora_task(self=self, task_name=title_task, url_task=href_task)
                    self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                logger.info("skip task")

            c += 1

    #### further tasks will go, but it will be better if there is a separate class for the back ####

    def finish(self):
        """
            The function that is responsible for checking the execution of the task
        """
        
        self.driver.implicitly_wait(10)
        logger.info("Function Finish")

        s = self.driver.find_element(By.CLASS_NAME, "full-width").find_elements(By.TAG_NAME, "button")
        for i in s:
            try:
                if i.text.strip() == "ПРОВЕРИТЬ":
                    sleep(1)
                    
                    i.click()
            
            except:
                logger.warning(f"Skip button finish")
                continue
        logger.info("Function Finish stop")
        
def main():
    Vktarget().vktarget()

if __name__ == '__main__':
    main()