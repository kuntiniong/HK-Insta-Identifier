from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import pandas as pd 
import time

class HypeAuditorScraper:
  # public:
  def scrape(self, gmail, password, hongkong):

    # approach:
    # intialize browser-> login google account -> login hypeauditor -> get the IG usernames ->
    # (parse HTML -> next page)* 20 pages -> store in a pandas DataFrame

    URL = "https://hypeauditor.com/top-instagram-all-hong-kong/" if hongkong == True else "https://hypeauditor.com/top-instagram-all-india/" # change -india to any country you wanna test out e.g. -united-states

    self._initializeDriver()
    self._googleLogin(gmail, password)
    self._hypeauditorLogin()
    self.driver.get(URL) 
    self.driver.implicitly_wait(1) 

    df = pd.DataFrame()
    for i in tqdm(range(20)): # 20 pages for 1000 results
      df = pd.concat([df, self._fetchData()], axis = 0, ignore_index = True)
      if i < 19:
        self._nextPage()
    self.driver.quit()

    return df


  # private:
  def _initializeDriver(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false') # disable the images to speed up 
    self.driver = webdriver.Chrome(options = chrome_options) 


  def _googleLogin(self, gmail, password):
    self.driver.get("https://www.gmail.com")

    email_element = self.driver.find_element(By.TAG_NAME, "input") 
    email_element.send_keys(gmail, Keys.ENTER) # input gmail

    time.sleep(5)

    password_element = self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    password_element.send_keys(password, Keys.ENTER) # input password


  def _hypeauditorLogin(self):
    self.driver.get("https://hypeauditor.com/login/")
    time.sleep(1)
    self.driver.find_element(By.XPATH, 
    '//*[@id="login-form-wrap"]/form[1]/div[1]/a').click() # press "use google login"
    time.sleep(2)
    self.driver.find_element(By.XPATH, 
    '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div').click() # press which account to login
    time.sleep(1)
    self.driver.find_element(By.XPATH, 
    '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div/div[2]/div/div/button').click() # press "continue"


  def _fetchData(self): # 50 results per page
    def objectToText(object_list, col_name): # .find_elements() method returns a list of objects
      return pd.DataFrame(data = [x.text for x in object_list], columns = [col_name])
    
    self.driver.implicitly_wait(1)
    username_list = objectToText(self.driver.find_elements(By.CLASS_NAME, "contributor__name-content"), "IG Username")
    return username_list


  def _nextPage(self): 
    time.sleep(1)

    actions = ActionChains(self.driver)
    actions.send_keys(Keys.HOME) # ensure the page is on the topmost
    for _ in range(6):
      actions.send_keys(Keys.PAGE_DOWN) # page down 6 times to locate the "next page" button
    actions.perform()

    time.sleep(2)

    button = self.driver.find_element(By.XPATH, 
    '//*[@id="__layout"]/div/div/div[2]/div/div[2]/div[1]/div[3]/button[2]/i') # press next page
    button.click()
