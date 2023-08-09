import discord
import scrython

from sqlalchemy import text
from sqlalchemy.orm import Session

from table2ascii import table2ascii as t2a, PresetStyle

from ..sql import sql_get_user_summary, sql_get_user_deck_summary

class UserStats(discord.Embed):

    def __init__(self, user_id, db_engine):
        super(UserStats, self).__init__(title=f"{user_id} Summary")

        with Session(db_engine) as session:
            res = session.execute(text(sql_get_user_summary), {'idplayer': user_id})
            user_stats = res.fetchall()
            res = session.execute(text(sql_get_user_deck_summary), {'idplayer': user_id})
            deck_stats = res.fetchall()

        if len(user_stats) > 0:
            wins, plays = user_stats[0]
            self.add_field(name=f"", value=f"{wins} wins, {plays} played", inline=False)
        else:
            self.add_field(name=f"Player ID not found", value="")

        if len(deck_stats) > 0:
            deck_str = "\n"
            for iddeck, comm, desc, color, wins, plays in deck_stats:
                deck_str += f"{iddeck} | {color} | {comm} | {desc} | {wins} wins, {plays} plays\n"
            self.add_field(name="Decks", value=deck_str, inline=False)


