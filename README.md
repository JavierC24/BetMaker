# BetMaker
A Python-based scraper for fetching, comparing and analyzing player data from Prizepicks API and Underdog API, coupled with a betting odds analyzer for various esports. The output is an HTML file showing the players that have a significant difference in score between the two platforms, along with their respective teams' betting odds.

# Esports Data Scraper and Odds Analyzer
Esports Data Scraper and Odds Analyzer is a Python script that fetches player data from Prizepicks and Underdog APIs, compares the player stats, and aligns them with their teams' betting odds from various esports websites. It filters and displays the players that have a significant difference in their statistics between the two platforms, along with their teams' betting odds. The results are saved to an HTML file and opened in your default web browser.

# Features
  Fetches player data from Prizepicks and Underdog APIs
  Analyzes and compares player stats
  Aligns player stats with their team's betting odds
  Filters and displays players with significant differences between the two platforms
  Saves results in an HTML file
  Usage
  python
  Copy code
if __name__ == "__main__":
    run_scraper(0.5)  # The argument represents the minimum difference in scores between the two platforms to consider

# Dependencies
The script requires the following Python packages to be installed:

  numpy
  pandas
  webbrowser
  re
  fuzzywuzzy
  tls_client
  Lines_With_Odds (local module, not a Python package)
You can install these packages with pip:
  pip install numpy pandas fuzzywuzzy

Please note, tls_client and Lines_With_Odds seem to be custom libraries or modules. They are not available as standard Python packages. You need to have these modules in your project's directory.

Output
The script outputs an HTML file named matching_players.html that includes the players with a significant difference in stats between the two platforms, along with their respective teams' betting odds. The HTML file is opened in a new tab in your default web browser after the script finishes running.

Future Improvements:
  Make the script interactive, allowing the user to input their own criteria for data filtering
  Implement more robust error handling
  Expand the sources of data to include more platforms and websites
  Contributions are more than welcome!

Disclaimer
This script is intended for personal use and should be used responsibly, in accordance with any terms of use or policies set out by the respective data sources.
