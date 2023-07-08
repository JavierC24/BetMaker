from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_website(url):
    # Set up the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the URL
    driver.get(url)

    # Wait for the page to fully render the dynamic content
    # Adjust the sleep time according to the page load time
    time.sleep(5)

    # Get the page source after rendering
    html = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Create a dictionary to store team names and odds
    team_odds_dict = {}

    # Find elements with class names "style_teamName__1Re1z", "style_teamName__BtxhI", "ellipsis", "style_drawTeamName__n-Rys"
    team_name_elements = soup.find_all(class_=["style_teamName__1Re1z style_teamName__BtxhI ellipsis style_drawTeamName__n-Rys"])

    # Find elements with class names "style_price__dFV4h", "style_drawPrice__3fXzx"
    price_elements = soup.find_all(class_=["style_price__dFV4h style_drawPrice__3fXzx"])

    # Match team names with corresponding odds and add them to the dictionary
    for team_name, odds in zip(team_name_elements, price_elements):
        team_odds_dict[team_name.text] = odds.text

    return team_odds_dict

