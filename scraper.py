import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Configuration
FILE_NAME = "sportdata.json"
URL = "https://www.madduxsports.com/line-moves.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def load_existing_data():
    """Loads existing JSON data or returns an empty list if it doesn't exist."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Warning: JSON file is empty or corrupted. Starting fresh.")
            return []
    return []

def scrape_odds_data():
    """Fetches and parses the odds data."""
    timestamp = datetime.utcnow().isoformat()
    
    # We structure the new data as a dictionary containing the time and the parsed games
    new_snapshot = {
        "scrape_timestamp_utc": timestamp,
        "games": []
    }
    
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- PARSING LOGIC ---
        # Note: You will need to inspect Maddux's specific table classes (e.g., <table class="lines">)
        # and extract the specific `tr` and `td` elements for NBA, NHL, and MLB.
        
        # Example placeholder logic showing how to append a game:
        # for row in table_rows:
        #     game_data = {
        #         "sport": "NBA", # Extracted from header
        #         "matchup": "Team A vs Team B",
        #         "open_line": -5.5,
        #         "current_line": -7.5,
        #         "ticket_pct": 42,
        #         "handle_pct": 68
        #     }
        #     new_snapshot["games"].append(game_data)
        
        # To ensure the script runs immediately without crashing before you write the parsing logic, 
        # I am appending a dummy record. Replace this with your BeautifulSoup extraction.
        new_snapshot["games"].append({
            "status": "Success",
            "message": "HTML fetched successfully. Add BeautifulSoup parsing logic here."
        })
        
        return new_snapshot

    except requests.exceptions.RequestException as e:
        print(f"Network error during scraping: {e}")
        return None

def main():
    print(f"Starting scrape run at {datetime.utcnow().isoformat()} UTC")
    
    # 1. Load historical data
    historical_data = load_existing_data()
    
    # 2. Scrape fresh data
    fresh_data = scrape_odds_data()
    
    # 3. Append and Save
    if fresh_data:
        historical_data.append(fresh_data)
        
        with open(FILE_NAME, "w") as file:
            # indent=4 keeps the JSON readable
            json.dump(historical_data, file, indent=4) 
        
        print(f"Successfully saved {len(historical_data)} total snapshots to {FILE_NAME}.")
    else:
        print("Scrape failed. No new data added.")

if __name__ == "__main__":
    main()
