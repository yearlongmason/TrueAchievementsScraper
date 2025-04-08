from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from random import uniform
import os
import dotenv

TIMEOUT: int = 10

def TALogin(driver, gamertag: str, password: str) -> bool:
    """Moves the driver to the login page and fills in relevant fields to login to the website
    Returns True if login was successful otherwise False"""
    # Go to login page
    driver.get("https://www.trueachievements.com/login")

    # Try to login using selenium
    try:
        # Wait until the text fields are on the page
        gamertagFieldPresent = EC.presence_of_element_located((By.ID, "txtGamerTag"))
        passwordFieldPresent = EC.presence_of_element_located((By.ID, "txtPassword"))
        loginButtonPresent = EC.presence_of_element_located((By.ID, "btnLogin"))
        WebDriverWait(driver, TIMEOUT).until(gamertagFieldPresent)
        WebDriverWait(driver, TIMEOUT).until(passwordFieldPresent)
        WebDriverWait(driver, TIMEOUT).until(loginButtonPresent)

        # Once the text fields are found, enter login information
        sleep(uniform(5,15))
        driver.find_element(By.ID , 'txtGamerTag').send_keys(gamertag)
        sleep(uniform(5,15))
        driver.find_element(By.ID , 'txtPassword').send_keys(password)
        sleep(uniform(5,15))
        driver.find_element(By.ID , 'btnLogin').click()
        sleep(uniform(5,15))
        #driver.execute_script(f"Postback('btnLogin_click')") # Sends javascript to console to login
    except:
        print("ERROR: Could not login!")
        return False
    return True

def parseTable(table: str) -> list[list[str]]:
    """Takes in table, a string that is HTML to build a table
    It returns a parsed version of the table"""
    soup = BeautifulSoup(table, 'html.parser')

    # Get all table rows in a list
    rows = soup.find_all("tr")
    fTable = [] # Keep track of formatted table list[list[str]]

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
        WebDriverWait(driver, TIMEOUT).until(element_present)

        # If found, return table HTML
        return driver.find_element(By.CLASS_NAME, gameCollectionTableClass).get_attribute('innerHTML')
    except:
        print("ERROR: Could not get the contents of the table!")

def moveToNextPage(driver, currentPage: int):
    """Moves to the next page on the game collection page and waits until it is done loading"""
    loadingDivID = "oGameCollection_Loading"

    # Send js to console to move to next page
    driver.execute_script(f"AJAXList.Buttons('oGameCollectionP','{currentPage + 1}')")

    # Wait until loading page is gone
    loadingDiv = driver.find_element(By.ID, loadingDivID)
    WebDriverWait(driver, TIMEOUT).until(lambda x: not loadingDiv.is_displayed())

def checkValidPage(driver) -> bool:
    """Try to find a warnings panel. If there is no warnings panel, then a NoSuchElementException will be raised
    That means the page is valid, so return True
    Otherwise, if there is a warnings panel on the page, that means it is invalid so return false"""
    warningsClass = "warningspanel"

    try:
        driver.find_element(By.CLASS_NAME, warningsClass)
        return False
    except NoSuchElementException:
        return True

def scrapeGameCollection(driver, searchGamertag: str) -> list[list[str]]:
    """Moves through each page, scrapes the table, and then appends new data"""
    # Go to game collection page
    driver.get(f"https://www.trueachievements.com/gamer/{searchGamertag}/gamecollection")
    currentPage = 1
    
    # Get game table header and add to gameTable [['row1', 'row2' ... 'rown']]
    gameTableHTML = scrapeGameCollectionTable(driver)
    gameTable = [parseTable(gameTableHTML)[0]] # Build game table formatted as list

    # Loop through all pages (Keep moving to the next page until the page is invalid)
    while checkValidPage(driver):
        # Get the HTML from the game table and add parsed rows to formatted game table (2d array)
        gameTableHTML = scrapeGameCollectionTable(driver)
        gameTable.extend(parseTable(gameTableHTML)[1:-1])

        # Move to the next page (and wait for it to stop loading)
        sleep(uniform(5,15))
        moveToNextPage(driver, currentPage)
        currentPage += 1

    # TEST PRINT
    #for row in gameTable:
    #    print(f"{row[1]} | {row[3]} | {row[8]}")

    return gameTable

def scrapeFromGamertag(gamertag: str) -> list[list[str]]:
    """Creates web driver and scrapes game collection"""
    # Load login credentials from env
    dotenv.load_dotenv()
    login_gamertag = os.getenv('gamertag')
    login_password = os.getenv('password')
    driver_path = os.getenv('driverPath')

    # Creating driver options
    options = webdriver.ChromeOptions()
    #options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable Automation flag
    options.add_argument("--disable-infobars")  # Prevent the "Chrome is being controlled" info bar
    options.add_argument("--no-sandbox")  # Prevent issues in some environments
    options.add_argument("--disable-dev-shm-usage")  # Workaround for headless mode issues
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--enable-javascript")  # Ensure JavaScript is enabled
    options.add_argument('--disable-popup-blocking') # Disable pop-up blocking
    options.binary_location = driver_path

    # Create driver
    driver = webdriver.Chrome(options=options)

    # Login to TrueAchievments and return scraped game collection
    TALogin(driver, login_gamertag, login_password)
    return scrapeGameCollection(driver, gamertag)

def timePlayedToMinutesPlayed(timePlayed: str) -> int:
    # If time played is an empty string then assume 0 minutes
    if not timePlayed:
        return 0
    
    # If the user has played more than an hour then it is formatted as XX hrs XX mins
    if "hrs" in timePlayed:
        hoursPlayed = int(timePlayed.split(" ")[0])
        minutesPlayed = int(timePlayed.split(" ")[2])
        return ((hoursPlayed * 60) + minutesPlayed)
    # If the user has played less than 1 hour then it is formatted as XX mins
    else:
        minutesPlayed = int(timePlayed.split(" ")[0])
        return minutesPlayed

def formatGameTableJSON(gameTable: list[list[str]]) -> list[dict[str:any]]:
    """Formats game table from scraper as json"""
    gameTableJSON = []
    
    # Loop through each row in the game table
    for game in gameTable[1:]:

        # Create a new dictionary for each game
        newGameDict = dict()
        for i, header in enumerate(gameTable[0]):
            if header in ["%age"]:
                newGameDict[header] = float(game[i])
            elif header not in ["", " ", "Notes"]:
                newGameDict[header] = game[i]
        newGameDict["Minutes played"] = timePlayedToMinutesPlayed(newGameDict["Time played"])

        # For now "My rating" doesn't give any useful information so we delete it
        # We might make use of this later
        del newGameDict["My rating"]
        newGameDict["Title"] = newGameDict["Title"].replace("'", "") # JUST FOR TESTING, REMOVE LATER

        # Append new game to the game table
        gameTableJSON.append(newGameDict)

    return gameTableJSON

if __name__ == "__main__":
    # Set the gamertag to search as a constant for now
    searchGamertag = "yearlongmason"

    gameTable = scrapeFromGamertag(searchGamertag)
    print(formatGameTableJSON(gameTable))