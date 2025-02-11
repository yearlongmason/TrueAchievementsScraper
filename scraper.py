from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

user = "yearlongmason"
gameTableID = "oGamerGamesList"

# Changing options
chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument('--ignore-certificate-errors-spki-list')
chromeOptions.add_argument("--ignore-certificate-errors")
chromeOptions.add_argument("--ignore-ssl-errors")

# Starting Chrome driver
driver = webdriver.Chrome(options=chromeOptions)
driver.get(f"https://www.trueachievements.com/gamer/{user}/games")

# Try to get the main games table element from the web page
try:
    # Wait until the element is present on the page
    element_present = EC.presence_of_element_located((By.ID, gameTableID))
    WebDriverWait(driver, 10).until(element_present)

    # If the element is found, send message to the terminal and get the table's content
    print("Found!")
    gameTable = driver.find_element(By.ID, gameTableID)
    #print(gameTable.get_attribute('innerHTML'))
except:
    print("There was an error trying to get that element!")
sleep(5)