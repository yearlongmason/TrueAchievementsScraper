# TrueAchievements Scraper

Welcome to the **TrueAchievements Stats Page**

This tool is designed to give Xbox gamers a clean, personalized way to view and explore their gaming stats by pulling data directly from [TrueAchievements.com](https://www.trueachievements.com).

---

## Our Mission

Tracking your gaming progress is fun — but Xbox's built-in tools and even third-party sites can sometimes feel overwhelming or not quite personal enough.  
We set out to create a sleek, focused dashboard that puts **your achievements** front and center in a way that’s both functional and fun to explore.

This project offers a simple and engaging way to visualize your gaming history. It combines **web scraping** with a **custom web interface** where you can:

- Explore fun statistics about your Xbox gaming history  
- Track your progress over time with clear visuals

---

## How to Run

To view your own Xbox stats — just follow these steps:

### 1. Go to your game collection  
Head over to: `https://www.trueachievements.com/gamer/{YourGamertag}/gamecollection`  
_(Replace `{YourGamertag}` with your actual Xbox gamertag)_

### 2. Download each page as HTML  
- Press `CTRL + S` (or `Cmd + S` on Mac) on **each page** of your game collection  
- Save the files as `.html` locally  
- Make sure to download **every page** if your collection spans multiple pages

### 3. Run the scraper  
In your terminal, run: `python staticTAScraper.py <page1.html> <page2.html> ... <pageN.html>`

- Replace `pageX.html` with the names of your downloaded HTML files  
- You can include as many pages as needed

### 4. View your stats  
Once the script finishes, open `index.html` in your browser and enjoy your personalized stats dashboard!

---

## The Tech Behind It

This project scrapes public user data from TrueAchievements and displays it on a dedicated stats page. Under the hood, it uses:

- Python  
- Selenium and BeautifulSoup for web scraping  
- Chart.js for clean, interactive data visualizations  
- HTML, Tailwind CSS, and JavaScript for a responsive frontend

---

## Get Involved

As an open source project, we welcome contributions!

Have a feature idea? Found a bug? Open an issue or submit a pull request — we’d love your input!

---

Happy achievement hunting!