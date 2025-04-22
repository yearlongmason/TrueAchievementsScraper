let gameTablePath = "./Scrapers/data/gameTable.json";
let gameData = null;

window.onload = async (event) => {
    // Call the function to load the data
    await fetchJson();
    updateHeader();
    renderMostPlayedGames();
    renderClosestTo100PercentChart();
    renderPlaytimeVSPercentage();
    renderCompletedVSNotCompleted();
    //console.log(gameTable)
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

function renderMostPlayedGames(){
    // Get top 10 most played games
    sortedGames = gameTable.sort((a, b) => a["Minutes played"] - b["Minutes played"])
    if(sortedGames.length > 10) {
        sortedGames = sortedGames.slice(sortedGames.length - 10)
    }

    const chartCanvas = document.getElementById('MostPlayedGameChart').getContext('2d');
    const chart = new Chart(chartCanvas, {
        type: "bar",
        data: {
            labels: sortedGames.map((game) => game.Title), // x axis labels
            datasets: [{
                label: 'Minutes Played',
                data: sortedGames.map((game) => game["Minutes played"]), // Y-axis data
                backgroundColor: '#2ecc71', // Bar color
                borderColor: '#2ecc71', // Border color
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const game = sortedGames[context.dataIndex]
                            return `Time Played: ${game["Time played"]}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Minutes Played',
                        font: {
                            size: 14
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Game Title',
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    })
}

function renderClosestTo100PercentChart(){
    // Get top 10 most played games
    sortedGames = gameTable.sort((a, b) => a["%age"] - b["%age"])
    sortedGames = sortedGames.filter((game) => game["%age"] != 100)
    if(sortedGames.length > 10) {
        sortedGames = sortedGames.slice(sortedGames.length - 10)
    }

    let lowestPercentage = Math.min(...sortedGames.map((game) => game["%age"]))

    const chartCanvas = document.getElementById('ClosestTo100PercentChart').getContext('2d');
    const chart = new Chart(chartCanvas, {
        type: "bar",
        data: {
            labels: sortedGames.map((game) => game.Title), // x axis labels
            datasets: [{
                label: '% Completed',
                data: sortedGames.map((game) => game["%age"]), // Y-axis data
                backgroundColor: '#2ecc71', // Bar color
                borderColor: '#2ecc71', // Border color
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const game = sortedGames[context.dataIndex]
                            return `${game["%age"]}% Completed`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: Math.max(lowestPercentage - 20, 0),
                    max: 100,
                    title: {
                        display: true,
                        text: 'Minutes Played',
                        font: {
                            size: 14
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Game Title',
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    })
}

function renderPlaytimeVSPercentage(){
    //console.log(gameTable)
    let timeVSPercentage = gameTable.map(game => { return {x: game["%age"], 
        y: game["Minutes played"],
    title: game["Title"],
    timePlayed: game["Time played"]} })

    const data = {
        datasets: [{
            label: 'Test Dataset',
            data: timeVSPercentage,
            backgroundColor: '#2ecc71'
        }]
    };

    const config = {
        type: 'scatter',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const game = timeVSPercentage[context.dataIndex]
                            return `${game.title} | ${game.x}% Completed | ${game.timePlayed}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Percent completed',
                        font: {
                            size: 14
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Minutes Played',
                        font: {
                            size: 14
                        }
                        
                    },
                    //type: "logarithmic"
                }
            }
        }
    };

    const chartCanvas = document.getElementById('PlaytimeVSPercentage').getContext('2d');
    new Chart(chartCanvas, config);
}

function renderCompletedVSNotCompleted(){
    let completedGames = gameTable.filter((game) => game["%age"] == 100).length;
    let inProgressGames = gameTable.filter((game) => game["%age"] != 100).length;

    const data = {
        labels: ['Completed', 'In Progress'],
        datasets: [{
            label: 'Game Progress',
            data: [completedGames, inProgressGames],
            backgroundColor: ['#2ecc71', '#2e2e2e'], // green and dark grey
            borderColor: ['#2ecc71', '#2e2e2e'],
            borderWidth: 1
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    };

    new Chart(document.getElementById('CompletedVSNotCompleted').getContext('2d'), config);
}