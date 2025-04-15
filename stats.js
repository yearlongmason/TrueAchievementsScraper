let gameTablePath = "./Scrapers/data/gameTable.json";
let gameData = null;

window.onload = async (event) => {
    // Call the function to load the data
    await fetchJson();
    updateHeader();
    console.log(gameTable)
    console.log(getTotalTimePlayed(gameTable))
};

async function fetchJson() {
  try {
    const response = await fetch(gameTablePath);
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    gameTable = data; // Save the JSON to the variable
    console.log('Game data loaded!');
  } catch (err) {
    console.error('Fetch error:', err);
  }
}

function formatMinutes(minutes) {
    return `${Math.floor(minutes / 60).toLocaleString()} Hours ${minutes % 60} Minutes`;
}

// Return the total time you've played across all games
function getTotalTimePlayed(gameTable) {
    let totalMinutesPlayed = gameTable.reduce((accumulator, currentValue) => accumulator + currentValue["Minutes played"], 0);
    return formatMinutes(totalMinutesPlayed);
}

function getTotalScore(gameTable, scoreType) {
    console.log(gameTable[0]["GS"].split(" / ")[0])
    let totalGS = gameTable.reduce((accumulator, currentValue) => accumulator + Number(currentValue[scoreType].split(" / ")[0].replace(/,/g, '')), 0);
    return totalGS.toLocaleString()
}

function getMostPlayedGame(gameTable) {
    let maxTimePlayed = gameTable[0]["Minutes played"];
    let mostPlayedGame = gameTable[0]["Title"];

    gameTable.forEach(game => {
        if (game["Minutes played"] > maxTimePlayed){
            maxTimePlayed = game["Minutes played"];
            mostPlayedGame = game["Title"];
        }
    });

    return `${mostPlayedGame} (${formatMinutes(maxTimePlayed)})`;
}

function updateHeader() {
    document.getElementById("totalTimePlayed").innerText = getTotalTimePlayed(gameTable)
    document.getElementById("totalGamerscore").innerText = getTotalScore(gameTable, "GS")
    document.getElementById("totalTrueAchievementsScore").innerText = getTotalScore(gameTable, "TA")
    document.getElementById("mostPlayedGame").innerText = getMostPlayedGame(gameTable)
}

// IF YOU GET A blocked by CORS policy ERROR:
// Copy and paste gameTable.json to the end of this line:
//let gameTable = 