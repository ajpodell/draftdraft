from lxml import html
import requests

import app as app_file
from models.base import db
from models.player import Player


def scrape_player_data():
    players = []
    page_count = 6
    # pages 5 and 6 error out, but keeping in case they get fixed
    for i in range(page_count):
        page = requests.get(
            f'https://www.drafttek.com/2023-NFL-Draft-Big-Board/Top-NFL-Draft-Prospects-2023-Page-{i + 1}.asp')
        tree = html.fromstring(page.content)
        name_elements = tree.xpath('//*[@id="rightbox"]/p')
        college_elements = tree.xpath('//*[@id="playerdata"]/div/p[1]')
        position_elements = tree.xpath('//*[@id="playerdata"]/div/p[2]')

        for j in range(len(name_elements)):
            full_name = name_elements[j].text.strip().split(" ")
            college_team = college_elements[j].text.strip()
            position = position_elements[j].text.strip()
            players.append(
                Player(
                    player_name_first=f'{full_name[0]}',
                    player_name_last=f'{full_name[1]}',
                    college_team=f'{college_team}',
                    position=f'{position}'
                )
            )

    return players


app = app_file.create_app()
with app.app_context():
    db.session.bulk_save_objects(scrape_player_data())
    db.session.commit()
