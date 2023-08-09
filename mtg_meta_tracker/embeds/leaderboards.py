import discord

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..sql import sql_deck_lb, sql_user_lb

class LBDeckEmbed(discord.Embed):

    def __init__(self, title, db_engine):
        super(LBDeckEmbed, self).__init__(title=title)

        with Session(db_engine) as session:
            res = session.execute(text(sql_deck_lb))
            decks = res.fetchall()

        for (deck_id, color, desc, comm, wins) in decks:
            if wins == 1:
                win_str = "win"
            else:
                win_str = "wins"
            self.add_field(name=f"{wins} {win_str}: {deck_id}",
                           value=f"{comm} - {desc}",
                           inline=False)

class LBUserEmbed(discord.Embed):

    def __init__(self, title, db_engine):
        super(LBUserEmbed, self).__init__(title=title)

        with Session(db_engine) as session:
            res = session.execute(text(sql_user_lb))
            user_records = res.fetchall()

        for (user, wins) in user_records:
            if wins == 1:
                win_str = "win"
            else:
                win_str = "wins"
            self.add_field(name="", value=f"{user} - {wins} {win_str}",
                           inline=False)
