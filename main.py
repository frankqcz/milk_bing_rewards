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

    @11/13/2017
    distinguishi between desktop awards and mobile awards.
    read account from disk.
    read search items from disk.
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime
import random

class account(object):
    def __init__(self, email, password, mode):
        super(account, self).__init__()
        self.email = email
        self.password = password
        self.current_points_desktop = 0
        self.earned_points_desktop = 0
        self.page_searches_desktop = 0
        self.current_points_mobile = 0
        self.earned_points_mobile = 0
        self.page_searches_mobile = 0

        if (mode == "desktop"):
            self.browser = webdriver.Firefox()
            #self.browser.get("https://www.whoishostingthis.com/tools/user-agent/")
            #time.sleep(5)
        elif (mode == "mobile"):
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", \
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1")
            self.browser = webdriver.Firefox(profile)
            #self.browser.get("https://www.whoishostingthis.com/tools/user-agent/")
            #time.sleep(5)
        else:
            print("Error: unidentified mode")
            return

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
        time.sleep(5)
        assert "Bing" in self.browser.title

    def earn_desktop_search_awards(self):
        ### print current points ###
        # the browser has to load the webpage again to make the points visible
        self.browser.get("https://bing.com")
        time.sleep(5)
        rewards = self.browser.find_element_by_id("id_rc")
        self.current_points_desktop = int(rewards.text)
        print("The current points are: ", rewards.text)
        initial_points = self.current_points_desktop
        target_points = 150
        while ((self.earned_points_desktop < target_points) and (self.page_searches_desktop<=40)):

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
                    self.page_searches_desktop += 1
                    time.sleep(random.randint(2,10))
                    try:
                        ### find a link and click into it ###
                        link = self.browser.find_element_by_partial_link_text(item[1:3])
                        print("Click the link:\t", link.text)
                        link.click()
                        time.sleep(random.randint(3,5))
                        self.browser.get("https://bing.com")
                        time.sleep(10)
                    except:
                        print("No Links")
                except:
                    print("Problem sending search item")

            ### Calculate the earned points ###
            rewards = self.browser.find_element_by_id("id_rc")
            self.current_points_desktop = int(rewards.text)
            print("The current points are: ", rewards.text)
            self.earned_points_desktop = self.current_points_desktop - initial_points
            print("Earned points are: ", self.earned_points_desktop)
            print("Searched times: ", self.page_searches_desktop)

    def earn_mobile_search_awards(self):
        ### print current points ###
        self.browser.get("https://m.bing.com")
        time.sleep(5)
        target_searches = 20
        while (self.page_searches_mobile <= target_searches):

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
                    self.page_searches_mobile += 1
                    time.sleep(random.randint(2, 10))
                    try:
                        ### find a link and click into it ###
                        link = self.browser.find_element_by_partial_link_text(item[1:3])
                        print("Click the link:\t", link.text)
                        link.click()
                        time.sleep(random.randint(3,5))
                        self.browser.get("https://m.bing.com")
                        time.sleep(5)
                    except:
                        print("No Links")
                except:
                    print("Problem sending search item")

            ### Calculate the earned points ###


    def get_current_points(self):
        self.browser.get("https://bing.com")
        time.sleep(5)
        rewards = self.browser.find_element_by_id("id_rc")
        self.current_points_desktop = int(rewards.text)
        print("The current points are: ", rewards.text)
        return self.current_points_desktop

    def quit(self):
        self.browser.quit()


if __name__ == "__main__":
    ### load search items ###
    search_items = []
    fn_search_items = "search_items.txt"
    try:
        fh_search_items = open(fn_search_items, 'r')
        for line in fh_search_items:
            search_items.append(line.strip())
    except:
        print("Cannot open the items file: ", fn_search_items)
    #print(search_items)

    ### load account and password information ###
    email = []
    password = []
    fn_account = "accounts.txt"
    try:
        fh_account = open(fn_account, 'r')
        for line in fh_account:
            usr, psw = [str(i) for i in line.split()]
            email.append(usr)
            password.append(psw)
    except:
        print("Cannot open the account file: ", fn_account)

    for i in range(len(email)):
        used_items = []

        ### earn mobile wards first ###
        milkBot = account(email[i],password[i], "mobile")
        milkBot.login()
        milkBot.earn_mobile_search_awards()
        #milkBot.get_current_points()
        time.sleep(3)
        milkBot.quit()
        time.sleep(3)

        ### earn desktop awards second ###
        milkBot = account(email[i],password[i], "desktop")
        milkBot.login()
        milkBot.earn_desktop_search_awards()
        #milkBot.get_current_points()
        time.sleep(3)
        milkBot.quit()
        time.sleep(3)
