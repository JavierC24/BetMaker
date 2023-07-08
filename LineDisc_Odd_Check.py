import numpy as np
import tls_client
import pandas as pd
import webbrowser
import re
from Lines_With_Odds import scrape_website
from fuzzywuzzy import fuzz, process

from ValKPR_Finder import find_expected_kills


def run_scraper(line_diff):
    # Set request headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }

    requests = tls_client.Session(client_identifier="chrome112")

    # Fetch data from Prizepicks API
    response1 = requests.get('https://api.prizepicks.com/projections', headers=headers)
    prizepicks = response1.json()

    # Fetch data from Underdog API
    request = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines", headers=headers)
    underdog = request.json()

    # Create empty lists to store player data
    udlist = []
    pplist = []
    matchingnames = []

    # Set to store unique player entries

    # Dictionary to store PrizePicks player name mappings
    library = {}

    for appearances in underdog["over_under_lines"]:
        # Extract player name from the title
        underdog_title = ' '.join(appearances["over_under"]["title"].split()[0:2])
        UDdisplay_stat = appearances['over_under']['appearance_stat']['display_stat']
        UDstat_value = appearances['stat_value']

        if ':' in underdog_title:
            UDdisplay_stat = UDdisplay_stat.split(' ')
            if '1+2' in UDdisplay_stat or '1+2+3' in UDdisplay_stat:
                UDdisplay_stat = f"Maps {UDdisplay_stat[-1].replace('+', '-')} {UDdisplay_stat[0]}"
            else:
                UDdisplay_stat = f"Map {UDdisplay_stat[-1]} {UDdisplay_stat[0]}"
            colon_index = underdog_title.find(":")
            underdog_title = underdog_title[colon_index + 1:].strip()
            uinfo = {"Name": underdog_title, "Stat": UDdisplay_stat, "Underdog": UDstat_value}
            udlist.append(uinfo)

    # Process PrizePicks API data
    for included in prizepicks['included']:
        if 'attributes' in included and 'name' in included['attributes']:
            PPname_id = included['id']
            PPname = included['attributes']['name']
            if 'team' in included['attributes']:
                ppteam = included['attributes']['team']
            else:
                ppteam = 'N/A'
            if 'league' in included['attributes']:
                ppleague = included['attributes']['league']
            else:
                ppleague = 'N/A'
            library[PPname_id] = {'name': PPname, 'team': ppteam, 'league': ppleague}

    for ppdata in prizepicks['data']:
        if '1st Half' in ppdata['attributes']['description']:
            continue
        PPid = ppdata['relationships']['new_player']['data']['id']
        PPprop_value = ppdata['attributes']['line_score']
        PPprop_type = ppdata['attributes']['stat_type']
        ppinfo = {"name_id": PPid, "Stat": PPprop_type, "Prizepicks": PPprop_value}
        pplist.append(ppinfo)

    # Iterate over the pplist array to add player names, team, and league, and remove name_id
    for element in pplist:
        name_id = element['name_id']
        if name_id in library:
            player_data = library[name_id]
            element['Name'] = player_data['name']
            element['Team'] = player_data['team']
            element['League'] = player_data['league']
        else:
            element['Name'] = "Unknown"
            element['Team'] = "N/A"
            element['League'] = "N/A"
        del element['name_id']

    # Compare player data from Underdog and PrizePicks
    for udn in udlist:
        for ppn in pplist:
            if udn["Name"].lower() == ppn["Name"].lower() and udn["Stat"].lower() == ppn["Stat"].lower():
                final = {
                    "Name": udn["Name"],
                    "Stat": udn["Stat"],
                    "Underdog": udn["Underdog"],
                    "Prizepicks": ppn["Prizepicks"],
                    "Team": re.sub(r'[^a-zA-Z0-9 ]', '', ppn["Team"]).strip(),
                    "League": ppn["League"]
                }
                matchingnames.append(final)

    # Create a DataFrame from the matching names
    rows = []
    for match in matchingnames:
        name = match['Name']
        stat = match['Stat']
        underdog_value = match['Underdog']
        prizepicks_value = match['Prizepicks']
        team = match['Team']
        league = match['League']
        rows.append((name, league, team, stat, underdog_value, prizepicks_value))
    df = pd.DataFrame(rows, columns=['Name', 'League', 'Team', 'Stat', 'Underdog', 'Prizepicks'])

    urls = [
        "https://www.pinnacle.com/en/esports-hub/csgo",
        "https://www.pinnacle.com/en/esports-hub/dota-2",
        "https://www.pinnacle.com/en/esports-hub/league-of-legends",
        "https://www.pinnacle.com/en/esports-hub/valorant"
    ]

    team_odds_library = {}

    for url in urls:
        data = scrape_website(url)

        # Add the scraped data to the team and odds library
        team_odds_library.update(data)
    # Iterate over the DataFrame rows
    for index, row in df.iterrows():
        team = row['Team']

        # Check if the team exists in the team_odds_library using fuzzy matching and abbreviation matching
        matched_team = None
        for library_team in team_odds_library.keys():
            # Here, token_set_ratio is used instead of partial_ratio
            if fuzz.token_set_ratio(team.lower(), library_team.lower()) >= 95:
                matched_team = library_team
                break
            elif fuzz.token_set_ratio(team.lower(), ''.join([char for char in library_team if char.isupper()])) == 100:
                matched_team = library_team
                break

        # If a match is found, update the 'Odds' column in the DataFrame with the matched odds
        if matched_team:
            odds = team_odds_library[matched_team]
            df.loc[index, 'Odds'] = odds
        else:
            # If no match is found, set the 'Odds' column as 'N/A' or any desired value
            df.loc[index, 'Odds'] = 'N/A'

    # Convert column values to float for numeric comparison
    df['Underdog'] = df['Underdog'].astype(float)
    df['Prizepicks'] = df['Prizepicks'].astype(float)

    # Filter the DataFrame based on the condition
    filtered_df = df[abs(df['Underdog'] - df['Prizepicks']) >= line_diff]
    filtered_df = filtered_df[filtered_df['Stat'] != 'Receiving Yards']

    scores_df_val = pd.read_csv('player_scores.csv')
    scores_df_notVal = pd.read_csv('player_lines_notVAL.csv')

    # Create a dictionary of player names and their expected kills
    expected_kills_val = dict(zip(scores_df_val['Nickname'].str.lower(), scores_df_val['Score']))
    expected_kills_notVal = {row['Name'].lower(): {'League': row['League'], 'Expected Kills': row['Expected Kills']} for index, row in scores_df_notVal.iterrows()}

    leagues = ['Dota2', 'LoL', 'CS:GO']

    # Add the "Expected Kills" column to the filtered_df DataFrame and populate it with the expected kills
    filtered_df.loc[filtered_df['League'] == 'VAL', 'Expected Kills'] = filtered_df.loc[
        filtered_df['League'] == 'VAL', 'Name'].str.lower().map(expected_kills_val)

    filtered_df.loc[filtered_df['League'].isin(leagues), 'Expected Kills'] = filtered_df.loc[
        filtered_df['League'].isin(leagues), 'Name'].str.lower().apply(
        lambda x: expected_kills_notVal[x]['Expected Kills'] if x in expected_kills_notVal else np.nan)

    def adjust_expected_kills(row):
        if row['League'] in ['Dota2', 'LoL'] and row['Stat'] == 'Maps 1-2 Kills':
            return row['Expected Kills'] * 2
        else:
            return row['Expected Kills']

    filtered_df['Expected Kills'] = filtered_df.apply(adjust_expected_kills, axis=1)
    filtered_df = filtered_df.sort_values(by='Odds', ascending=False)
    filtered_df.replace('N/A', np.nan, inplace=True)
    filtered_df.dropna(inplace=True)

    # Save the filtered DataFrame as an HTML file
    filtered_df.to_html('matching_players.html', index=False)

    # Open the HTML file in the default web browser
    webbrowser.open('matching_players.html', new=2)


if __name__ == "__main__":
    run_scraper(0.5)
