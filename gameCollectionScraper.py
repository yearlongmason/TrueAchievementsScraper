from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import os
import dotenv

def TALogin(driver, gamertag: str, password: str) -> bool:
    """This function will move the driver to the login page and fill in the relevant fields to login to the website
    Returns True if login was successful otherwise False"""
    # Go to login page
    driver.get("https://www.trueachievements.com/login")

    # Try to login using selenium
    try:
        # Wait until the text fields are on the page
        gamertagFieldPresent = EC.presence_of_element_located((By.ID, "txtGamerTag"))
        passwordFieldPresent = EC.presence_of_element_located((By.ID, "txtPassword"))
        loginButtonPresent = EC.presence_of_element_located((By.ID, "btnLogin"))
        WebDriverWait(driver, 10).until(gamertagFieldPresent)
        WebDriverWait(driver, 10).until(passwordFieldPresent)
        WebDriverWait(driver, 10).until(loginButtonPresent)

        # Once the text fields are found, enter login information
        driver.find_element(By.ID , 'txtGamerTag').send_keys(gamertag)
        driver.find_element(By.ID , 'txtPassword').send_keys(password)
        driver.find_element(By.ID , 'btnLogin').click()
    except:
        print("ERROR: Could not login!")
        return False
    return True

def parseTable(table: str) -> list[list[str]]:
    """This function takes in table, a string that is html for a table
    It returns a parsed version of the table"""
    soup = BeautifulSoup(table, 'html.parser')

    # Get all table rows in a list
    rows = soup.find_all("tr")
    # Keep track of formatted table list[list[str]]
    fTable = []

    # Add headers to the row
    fTable.append([])
    for th in rows[0].find_all("th"):
        fTable[-1].append(th.text)

    # Loop through all rows after the first one
    for row in rows[1:]:
        # Loop through every td tag in each row and append the text to the last list in the formatted table list
        fTable.append([])
        for td in row.find_all("td"):
            fTable[-1].append(td.text)

    return fTable

def scrapeGameCollectionTable(driver):
    """Takes the table that's on the page and scrapes it
    Returns the raw HTML inside the table"""
    gameCollectionTableClass = "maintable"

    # Try to get the main games table element
    try:
        # Wait until the table is on the page
        element_present = EC.presence_of_element_located((By.CLASS_NAME, gameCollectionTableClass))
        WebDriverWait(driver, 10).until(element_present)

        return driver.find_element(By.CLASS_NAME, gameCollectionTableClass).get_attribute('innerHTML')
    except:
        print("ERROR: Could not get the contents of the table!")

def scrapeGameCollection(driver, searchGamertag: str):
    """Moves through each page, scrapes the table, and then appends new data"""
    driver.get(f"https://www.trueachievements.com/gamer/{searchGamertag}/gamecollection")
    
    # Test print out
    gameTableHTML = scrapeGameCollectionTable(driver)
    for i in parseTable(gameTableHTML)[0:-1]:
        print(f"{i[1]} | {i[3]} | {i[8]}")


if __name__ == "__main__":
    # Set the gamertag to search as a constant for now
    searchGamertag = "yearlongmason"

    # Load login credentials from env
    dotenv.load_dotenv()
    login_gamertag = os.getenv('gamertag')
    login_password = os.getenv('password')

    # Creating driver options
    chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument('--ignore-certificate-errors-spki-list')
    chromeOptions.add_argument("--ignore-certificate-errors")
    chromeOptions.add_argument("--ignore-ssl-errors")

    # Starting Chrome driver
    driver = webdriver.Chrome(options=chromeOptions)
    TALogin(driver, login_gamertag, login_password)
    scrapeGameCollection(driver, searchGamertag)