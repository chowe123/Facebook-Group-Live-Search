from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

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

driver = webdriver.Chrome(chrome_options=option)
driver.implicitly_wait(10)

'''
loginFacebook (boolean): string, string, selenium driver
Logins in to facebook using the credentials and driver specified
Returns True if successful, false if not
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


def parsePost(postElement):
    postText = postElement.text.split('\n')
    postText = list(filter(lambda x:any(char.isalpha() or char.isdigit() for char in x) and len(x) > 5, postText))
    name = postText[0]
    post = postText[1]
    return (name, post)
    

group = 'https://www.facebook.com/groups/225049564330328?sorting_setting=CHRONOLOGICAL'

def getGroupPosts(groupURL, waitTime):
    returnPosts = []
    driver.get(groupURL)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(waitTime)
    feed = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div[1]/div[2]/div[2]")
    posts = feed.find_elements(By.XPATH, './*')[1:]
    for post in posts:
        try:
            returnPosts.append(parsePost(post))
        except:
            continue
    return returnPosts

newPosts = {}

print(loginFacebook('idontknowthispart@gmail.com', 'Ttws1n11234k5!', driver))

def liveSearch():
    oldPosts = {}
    while True:
        newPosts = getGroupPosts(group, 10)
        difference = set(newPosts) - set(oldPosts)
        if len(difference) > 0:
            print(difference)
        oldPosts = set(newPosts)

liveSearch()

