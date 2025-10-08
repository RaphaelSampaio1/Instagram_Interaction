import time 
from time import sleep
import random
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import logging
import traceback


from to_follow import InstagramBot


USERNAME = os.environ.get("IG_USERNAME") or input("Instagram username: ")
PASSWORD = os.environ.get("IG_PASSWORD") or input("Instagram password: ")

bot = InstagramBot(USERNAME, PASSWORD) # Create bot instance
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s') # Configure logging error level


class ReelInteractor:
    comment_list = [
        "This is fire!",
        "My algorithm is going blessed!",
        "Daaaaa I love this type of content!",
        "This is so cool!",
        "The best place ever !"
    ]
    

    @staticmethod
    def like_reel():
        try:
            actions = ActionChains(bot.driver) # Actions like Double Click, Right Click, etc.            
            element = "//div[@class='x1ypdohk' and @data-visualcompletion='ignore-dynamic']//div[@role='button']" 
            btn = WebDriverWait(bot.driver, 10).until(EC.element_to_be_clickable((By.XPATH, element)))

            actions.double_click(btn).perform()   #.perform() is required — it executes the queued actions.
        except Exception as e:
            logging.erro(f"Exception ocurred: ", exc_info=True)


    @staticmethod
    def comment_reel():
        try:
            xpath = "//div[@aria-expanded='false' and @aria-haspopup='menu' and @role='button']"
            btn = WebDriverWait(bot.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()
            
            sleep(random.uniform(2, 4))
    
            xpath_input = "//input[contains(@placeholder, 'Add a comment')]"
            input_box = WebDriverWait(bot.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_input)))
            input_box.click()
            
            editor_xp = "//div[@contenteditable='true' and @role='textbox' and @data-lexical-editor='true']"
            editor = WebDriverWait(bot.driver, 10).until(EC.visibility_of_element_located((By.XPATH, editor_xp)))
            bot.driver.execute_script("arguments[0].focus();", editor)
            comment_text = random.choice(ReelInteractor.comment_list)

            # Send Comment
            
            
            for char in comment_text:
                editor.send_keys(char)
                sleep(random.uniform(0.05, 0.15))
            
            bot.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", editor)
            sleep(random.uniform(1, 2))
            
            editor.send_keys(Keys.RETURN) ## Press Enter to submit
            sleep(random.uniform(2, 4))
            
        except Exception as e:
            logging.error(f"Exception ocurred: ", exc_info=True)


########## Main ##########
try:
    bot.login()
    
    bot.driver.get("https://www.instagram.com/reels/")
    sleep(random.uniform(2, 5))
    
    # Actually use the methods
    ReelInteractor.like_reel()
    sleep(random.uniform(5,6))
    ReelInteractor.comment_reel()
    
##########################
    print("Done!")
    sleep(99)
##########################

finally:
    bot.close()