let gameTablePath = "./Scrapers/data/gameTable.json";

async function fetchJson() {
    try {
      const response = await fetch(gameTablePath);
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();
      return data;
    } catch (err) {
      console.error('Fetch error:', err);
      return null;
    }
  }
  
  fetchJson().then(data => {
    console.log(data);
  });