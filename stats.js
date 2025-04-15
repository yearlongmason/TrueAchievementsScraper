let gameTablePath = "./Scrapers/data/gameTable.json";
let gameData = null;

window.onload = async (event) => {
    // Call the function to load the data
    await fetchJson();
    console.log(gameTable)
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