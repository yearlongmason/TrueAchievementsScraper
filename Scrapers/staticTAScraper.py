"""
This file should be run as python .\staticTAScraper.py <filename1.html> <filename2.html> ... <filenameN.html>
This will scrape the static files for data needed for the TrueAchievements stats page
The files provided should be each page from the users game collection on true achievements
This will output the data as a json file
"""

import argparse
import json
from bs4 import BeautifulSoup

def getData(fileName: str) -> str:
    """Returns the contents of a file as a string"""
    with open(f"./data/{fileName}") as file:
        return file.read()
    
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

def scrapeFiles(files: list[str]) -> list[list[str]]:
    # Get a game table and add the header row as the first row
    headerRow = parseTable(getData(files[0]))[0]
    gameTable = [headerRow]
    
    # Loop through each file, get the html, and parse the table
    for file in files:
        htmlFile = getData(file)
        # Append each row (each game) to the gameTable
        for game in parseTable(htmlFile)[1:]:
            gameTable.append(game)

    return gameTable

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
    """Formats game table from scraper as JSON"""
    gameTableJSON = []
    
    # Loop through each row in the game table
    for game in gameTable[1:]:

        # Create a new dictionary for each game
        newGameDict = dict()
        # Loop through each game table header
        for i, header in enumerate(gameTable[0]):
            # Cast selected values as floats
            if header in ["%age"]:
                newGameDict[header] = float(game[i]) if game[i] else 0

            # If the header is not empty then try to cast as JSON
            elif header not in ["", " ", "Notes"]:
                try:
                    newGameDict[header] = game[i]
                except IndexError:
                    pass

        # Add minutes played to JSON
        newGameDict["Minutes played"] = timePlayedToMinutesPlayed(newGameDict["Time played"])

        # For now "My rating" doesn't give any useful information so we delete it
        # We might make use of this later
        del newGameDict["My rating"]
        #newGameDict["Title"] = newGameDict["Title"].replace("'", "") # JUST FOR TESTING, REMOVE LATER

        # Append new game to the game table if it has a title
        if newGameDict["Title"]:
            gameTableJSON.append(newGameDict)

    return gameTableJSON

def saveGameTableAsJSON(saveTo: str, gameTableJSON: list[dict[str:any]]):
    with open(saveTo, 'w') as outfile:
        json.dump(gameTableJSON, outfile,indent=4)

if __name__ == "__main__":
    # Get arguments given to Python 
    parser = argparse.ArgumentParser(description='Static True Achievement Scraper')
    parser.add_argument('files', nargs='*', help='Static True Achievements html files to scrape')
    files = parser.parse_args().files

    # If no files are provided set files to default test files
    if not files:
        files = ['yearlongmason1.html', 'yearlongmason2.html', 
                 'yearlongmason3.html', 'yearlongmason4.html', 
                 'yearlongmason5.html', 'yearlongmason6.html']

    # Scrape files and save data as JSON
    gameTable = scrapeFiles(files)
    gameTableJSON = formatGameTableJSON(gameTable)
    saveGameTableAsJSON("./data/gameTable.json", gameTableJSON)