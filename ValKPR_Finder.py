import csv
import tls_client


def calculate_player_scores(stats):
    player_scores = []

    for player in stats['players']:
        nickname = player['nickname'].lower()  # Convert nickname to lowercase
        rounds_played = int(player['roundsPlayed'])
        kills_per_round = float(player['killsPerRound'])
        score = 48 * kills_per_round
        player_scores.append({'Nickname': nickname, 'Score': score})

    return player_scores


def find_expected_kills():
    link = "https://api.thespike.gg/stats/players?rounds=100"
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

    valorant_stat_find = requests.get(link)
    stats = valorant_stat_find.json()

    scores = calculate_player_scores(stats)

    with open('player_scores.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nickname', 'Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(scores)


if __name__ == "__main__":
    find_expected_kills()
