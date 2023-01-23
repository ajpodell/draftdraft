#!/usr/bin/env python
""" Tool to run the db setup command.

Theres probably a cleaner way to do this, but this is what I've got.

Note: all models must be imported for this to work. Not sure if thats always needed, but, again, what all i know so far.
"""
import click

import app as app_file
from blueprints import auth_blueprint
from models import (
    base,
    player,
    selection,
    user,
)
from dev_tools import player_scraper


class DraftSetup:
    @staticmethod
    def insert_teams():
        click.echo('inserting teams')

        teams = [
            'aaron', 'Shayna', 'Dan', 'greg', 'Jason', 'Zack', 'Riv',
        ]
        app = app_file.create_app()
        with app.app_context():
            base.db.init_app(app)
            for team in teams:
                auth_blueprint.create_user(team, team)

            base.db.session.query(user.User).filter_by(username='aaron').update({user.User.is_admin: True})
            base.db.session.query(user.User).filter_by(username='greg').update({user.User.is_admin: True})
            base.db.session.commit()

    @staticmethod
    def insert_players():
        click.echo('inserting players')
        player_scraper.scrape_players()

    @staticmethod
    def create_tables():
        """ switch this to use the code equivalent of `flask db upgrade`"""
        print('creating tables')
        return
        app = app_file.create_app()
        with app.app_context():
            base.db.init_app(app)
            base.db.create_all()


@click.command()
@click.option("--create-tables", is_flag=True, show_default=True, default=False, help="create the tables")
@click.option("--insert-teams", is_flag=True, show_default=True, default=True, help="insert dummy teams")
@click.option("--insert-players", is_flag=True, show_default=True, default=True, help="Run the player scraper and insert players.")
def main(create_tables, insert_teams, insert_players):
    draft_setup = DraftSetup()

    # maybe moe this to the draft setup directly
    if create_tables:
        click.echo('dont use this anymore. were on alembic - use `flask db upgrade/downgrade`')

    if insert_teams:
        draft_setup.insert_teams()

    if insert_players:
        draft_setup.insert_players()
    
if __name__ == '__main__':
    main()




