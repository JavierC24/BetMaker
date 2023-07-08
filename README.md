# Esports Data Scraper and Odds Analyzer

Esports Data Scraper and Odds Analyzer is a Python script that fetches player data from Prizepicks and Underdog APIs, compares the player stats, and aligns them with their teams' betting odds from various esports websites. It filters and displays the players that have a significant difference in their statistics between the two platforms, along with their teams' betting odds. The results are saved to an HTML file and opened in your default web browser.

## Features

- Fetches player data from Prizepicks and Underdog APIs
- Analyzes and compares player stats
- Aligns player stats with their team's betting odds
- Filters and displays players with significant differences between the two platforms
- Saves results in an HTML file

## Usage

```python
if __name__ == "__main__":
    run_scraper(0.5)  # The argument represents the minimum difference in scores between the two platforms to consider
```

The script also uses tls_client and Lines_With_Odds which appear to be custom libraries or modules and aren't standard Python packages. You will need to have these modules in your project directory.

## Output
The script outputs an HTML file `matching_players.html`. This file includes the players with a significant difference in their statistics between the two platforms, along with their team's betting odds.

## Contributing
Contributions are always welcome. Please ensure to update tests as appropriate. For major changes, please open an issue first to discuss what you would like to change.

## Future Enhancements
- **Interactive Scripting**: Enabling users to input their own criteria for data filtering.
- **Robust Error Handling**: Implementing a more efficient way of handling errors.
- **Expand Data Sources**: Including more platforms and websites for a wider data comparison.

## Disclaimer
This script is intended for personal use. Ensure to use it responsibly, and abide by the terms of use or policies from the respective data sources.

## Requirements

To run this script, there are certain requirements:

1. **Python Environment**: You need to have Python installed on your system (version 3.6 or later recommended).

2. **Dependencies**: Make sure to install all the dependencies mentioned in the 'Installation' section. You can use pip to install these packages.

3. **Data Scrapping Functions**: The script requires `scrape_website` and `find_expected_kills` functions to scrape data from websites and find expected kills respectively. Ensure these functions are defined in your Python environment and working properly. If you are running this script in a standalone manner, make sure these functions are included in your script or imported from the necessary modules.

## Installation

To install the required dependencies, you can use pip, which is a package manager for Python. Run the following command in your terminal:

```bash
pip install pandas numpy fuzzywuzzy requests lxml beautifulsoup4


