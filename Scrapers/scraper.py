from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
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

def parseTable(table: str) -> list[list[str]]:
    """This function takes in table, a string that is html for a table
    It returns a parsed version of the table"""
    soup = BeautifulSoup(table, 'html.parser')

    # Get all table rows in a list
    rows = soup.find_all("tr")

    # Keep track of formatted table list[list[str]]
    fTable = []

    # Add headers to the first list
    fTable.append([])
    for th in rows[0].find_all("th"):
        fTable[-1].append(th.text)

    # Loop through all rows after first
    for row in rows[1:]:
        # Loop through every td tag in each row and append the text to the last list in the formatted table list
        fTable.append([])
        for td in row.find_all("td"):
            fTable[-1].append(td.text)

    return fTable

# Try to get the main games table element from the web page
try:
    # Wait until the element is present on the page
    element_present = EC.presence_of_element_located((By.ID, gameTableID))
    WebDriverWait(driver, 10).until(element_present)

    # If the element is found, send message to the terminal and get the table's content
    print("Found!")
    gameTable = driver.find_element(By.ID, gameTableID)
    gameTable = gameTable.get_attribute('innerHTML')
except:
    print("There was an error trying to get that element!")
driver.quit() # If we find what we're looking for we can close the driver

parseTable(gameTable)