"""
This bot uses the selenium library to get bing awards
Firefox and Edge browsers work.
Chrome will crash.

Update log:
    @11/10/2017
    successfully login to outlook accout.

    @11/11/2017
    add current reward points checker
    add desktop_search_awards function
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime
import random

class account(object):
    def __init__(self, email, password):
        super(account, self).__init__()
        self.email = email
        self.password = password
        self.current_points = 0
        self.earned_points = 0
        self.page_searches = 0
        self.browser = webdriver.Firefox()


    def login(self):
        #browser = webdriver.Firefox()
        self.browser.get("https://login.live.com")
        time.sleep(3)
        emailField = self.browser.find_element_by_id("i0116")
        emailField.send_keys(self.email)
        time.sleep(1)
        emailField.send_keys(Keys.ENTER)
        time.sleep(3)
        passwordField = self.browser.find_element_by_id("i0118")
        passwordField.send_keys(self.password)
        time.sleep(1)
        passwordField.send_keys(Keys.ENTER)
        time.sleep(10)
        self.browser.get("https://bing.com")
        time.sleep(10)
        assert "Bing" in self.browser.title
    def earn_desktop_search_awards(self):
        ### print current points ###


        ### find the search bar ###
        searchbar = self.browser.find_element_by_id("sb_form_q")

        ### delete everything in the search bar ###
        searchbar.send_keys(Keys.CONTROL, 'a')
        searchbar.send_keys(Keys.DELETE)
        time.sleep(3)

        ### generate a random term to searchbar ###
        item = search_items[random.randrange(0, len(search_items))]
        print("Searching for:\t", item)

        try:
            ### enter the search item ###
            searchbar.send_keys(item)
            time.sleep(2)
            searchbar.send_keys(Keys.ENTER)
            self.page_searches += 1
            time.sleep(random.randint(5,20))

            try:
                ### find a link and click into it ###
                link = self.browser.find_element_by_partial_link_text(item[1:3])
                print("Click the link:\t", link.text)
                link.click()
                time.sleep(random.randint(3,8))
                self.browser.back()
            except:
                print("No Links")
        except:
            print("Problem sending search item")
        time.sleep(3)

    def get_current_points(self):
        self.browser.get("https://bing.com")
        time.sleep(5)
        rewards = self.browser.find_element_by_id("id_rc")
        self.current_points = int(rewards.text)
        return self.current_pints()

    def quit(self):
        self.browser.quit()


if __name__ == "__main__":
    search_items = ["facebook", "twitter", "Linkedin", "Glassdoor","Indeed",\
                    "microsoft", "Google", "map","yelp", "google scholar"]
    email = "email"
    password = "password"
    milkBot = account(email,password)
    milkBot.login()
    milkBot.earn_desktop_search_awards()
    milkBot.get_current_points()
    time.sleep(3)
    milkBot.quit()
