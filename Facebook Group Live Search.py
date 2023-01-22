from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from playsound import playsound
import re

sound = r"C:\Users\Admin\Desktop\Facebook LiveSearch\notificationSound.wav"


option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

driver = webdriver.Chrome(options=option)
driver.implicitly_wait(10)

'''
loginFacebook (boolean): string, string, selenium driver
    Logins in to facebook using the credentials and driver specified
    Returns True if logged in successfully, false if not
'''
def loginFacebook(username, password, driver):
    driver.get("https://www.facebook.com/")
    usernameField = driver.find_element(By.XPATH, '//*[@id="email"]')
    passwordField = driver.find_element(By.XPATH, '//*[@id="pass"]')
    loginButton = driver.find_element(By.NAME, 'login')
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    loginButton.click()
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Friends')]")
    except:
        return False
    return True

'''
parsePost (tuple): selenium web element
    Takes a facebook group post element and returns the post in the following format (Author, Post text)
'''
def parsePost(postElement):
    postText = postElement.text.split('\n')
    postText = list(filter(lambda x: any(char.isalpha() or char.isdigit() for char in x) and len(x) > 3, postText))
    name = postText[0]
    endIndex = postText.index("Like")
    if "All reactions:" in postText:
        endIndex = postText.index("All reactions:")
    post = str(postText[1:endIndex])
    return (name, post)

'''
getGroupPosts (lst of post elements): string, int, selenium driver
Takes a facebook group link, an time to wait, and a web driver and returns the first 10 posts
'''
def getGroupPosts(groupURL, waitTime, driver):
    returnPosts = []
    driver.get(groupURL)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(waitTime)
    try:
        feed = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div[1]/div[2]/div[2]")
    except:
        return False
    posts = feed.find_elements(By.XPATH, './*')[1:]
    for post in posts:
        try:
            returnPosts.append(parsePost(post))
        except:
            continue
    return returnPosts[:min(10, len(returnPosts))]

'''
liveSearch (None): list of strings, string
Takes a facebook group link and prints/plays a sound if a new post matches the criteria
'''
def liveSearch(mustContain, url):
    oldPosts = set()
    while True:
        newPosts = getGroupPosts(url, 10, driver)
        if newPosts == False:
            print('Page failed to load, trying again...')
            continue
        difference = set(newPosts) - set(oldPosts)
        if len(difference) > 0:
            print(len(difference))
            oldPosts = oldPosts.union(set(newPosts))
            filteredPosts = [post for post in difference if any(mKey.upper() in post[1].upper() for mKey in mustContain)]
            filteredPosts = [post for post in filteredPosts if not 'LOOKING' in post[1].upper()]
            if len(filteredPosts) > 0:
                for post in filteredPosts:
                    print(post)
                playsound(sound)

if __name__ == "__main__":
    group = 'https://www.facebook.com/groups/225049564330328?sorting_setting=CHRONOLOGICAL'
    credentials = 'C:\\Users\\Admin\\Desktop\\Facebook LiveSearch\\Credentials.txt'
    userPass = open(credentials, "r").read().split('\n')
    if loginFacebook(userPass[0], userPass[1], driver):
        #regexFilter = "^(?!.*\blooking\b)(?=.*(mark|mk|fmp|unionville|scar|sk|rich|rch|time)).*$"
        #newPosts = getGroupPosts(group, 10, driver)
        liveSearch(['mark', 'mk', 'fmp', 'unionville', 'scar', 'sk', 'rich', 'rch', 'time'], group)

