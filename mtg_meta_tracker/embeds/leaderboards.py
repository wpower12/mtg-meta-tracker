import discord

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..util import colors_to_str_rep
from ..sql import sql_deck_lb

class LBDeckEmbed(discord.Embed):

    def __init__(self, title, db_engine, emojis):
        super(LBDeckEmbed, self).__init__(title=title)

        with Session(db_engine) as session:
            res = session.execute(text(sql_deck_lb))
            decks = res.fetchall()

        for (deck_id, color, desc, comm, wins) in decks:
            color_rep = colors_to_str_rep(color, emojis)
            if wins == 1:
                win_str = "win"
            else:
                win_str = "wins"
            self.add_field(name=f"{wins} {win_str}: {deck_id}; {comm}",
                           value=f"{color_rep} - {desc} ",
                           inline=False)
