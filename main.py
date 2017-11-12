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

    @11/12/2017
    add while loop to keep earning desktop search awards until 150 points
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
        rewards = self.browser.find_element_by_id("id_rc")
        self.current_points = int(rewards.text)
        print("The current points are: ", rewards.text)
        initial_points = self.current_points
        target_points = 150
        used_items = []
        while ((self.earned_points < target_points) and (self.page_searches<=40)):

            ### find the search bar ###
            searchbar = self.browser.find_element_by_id("sb_form_q")

            ### delete everything in the search bar ###
            searchbar.send_keys(Keys.CONTROL, 'a')
            searchbar.send_keys(Keys.DELETE)
            time.sleep(3)

            ### generate a random term to searchbar ###
            item = search_items[random.randrange(0, len(search_items))]
            if item not in used_items:
                used_items.append(item)
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
                        time.sleep(random.randint(5,10))
                        self.browser.get("https://bing.com")
                        time.sleep(5)
                    except:
                        print("No Links")
                except:
                    print("Problem sending search item")

            time.sleep(5)
            ### Calculate the earned points ###
            rewards = self.browser.find_element_by_id("id_rc")
            self.current_points = int(rewards.text)
            print("The current points are: ", rewards.text)
            self.earned_points = self.current_points - initial_points
            print("Earned points are: ", self.earned_points)
            print("Searched times: ", self.page_searches)



    def get_current_points(self):
        self.browser.get("https://bing.com")
        time.sleep(5)
        rewards = self.browser.find_element_by_id("id_rc")
        self.current_points = int(rewards.text)
        return self.current_points

    def quit(self):
        self.browser.quit()


if __name__ == "__main__":
    search_items = ["what is facebook", "how twitter", "Linkedin", "Glassdoor","Indeed",\
                    "microsoft", "Google", "map","yelp", "google scholar",\
                    "UCI location", "UCLA email", "USC fun", "Team up", \
                    "Starcraft I", "trump", "white left", "Friends"\
                    "frankqcz", "Github usage", "APDSL website", "apple music",\
                    "Reddit login", "Dictionary text", "shengciben",\
                    "Zootopia on screen", "Tustin AMC", "Maxlinear corp", \
                    "Broadcom buy qualcomm", "Xinks stock", "Des Auto", \
                    "when game of throne ends", "Bing vs Google"]
    email = "email"
    password = "password"
    milkBot = account(email,password)
    milkBot.login()
    milkBot.earn_desktop_search_awards()
    milkBot.get_current_points()
    time.sleep(3)
    milkBot.quit()
