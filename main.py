"""
This bot uses the selenium library to get bing awards
It works a Firefox window. Firefox is preferred, because Chrome will crash.

Update log:
    @11/10/2017
    successfully login to outlook accout.

"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime

class account(object):
    def __init__(self, email, password):
        super(account, self).__init__()
        self.email = email
        self.password = password
        self.current_points = 0
        self.earned_points = 0
        self.page_searches = 0

    def login(self):
        browser = webdriver.Firefox()
        browser.get("https://login.live.com")
        time.sleep(3)
        emailField = browser.find_element_by_id("i0116")
        emailField.send_keys(self.email)
        time.sleep(1)
        emailField.send_keys(Keys.ENTER)
        time.sleep(3)
        passwordField = browser.find_element_by_id("i0118")
        passwordField.send_keys(self.password)
        time.sleep(1)
        passwordField.send_keys(Keys.ENTER)




if __name__ == "__main__":
    email = "email"
    password = "password"
    milkBot = account(email,password)
    milkBot.login()
