from fastapi import FastAPI
from gameCollectionScraper import scrapeFromGamertag, formatGameTableJSON
# To run this api: Open a terminal and navigate to the api folder
# Then run "uvicorn TAScraperAPI:app --reload"
# Might have to run "pip install uvicorn" or "pip install fastapi" if not already installed
# Great tutorial for using fastapi: https://www.youtube.com/watch?v=tLKKmouUams

app = FastAPI()

# Default api state
@app.get("/")
async def testAPIMessage():
    return {"Hello":"FastAPI!"}

# Get data for a user
@app.get("/gameCollection")
async def getGameCollection(gamertag: str):
    gameTable = scrapeFromGamertag(gamertag)
    return formatGameTableJSON(gameTable)