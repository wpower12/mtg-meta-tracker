import discord

from ..util import colors_to_str_rep
from ..sql import sql_deck_lb

class LBDeckEmbed(discord.Embed):

    def __init__(self, title, cnx, emojis):
        super(LBDeckEmbed, self).__init__(title=title)

        cur = cnx.cursor()
        cur.execute(sql_deck_lb)
        for (deck_id, color, desc, comm, wins) in cur:
            color_rep = colors_to_str_rep(color, emojis)
            if wins == 1:
                win_str = "win"
            else:
                win_str = "wins"
            self.add_field(name=f"{wins} {win_str}: {deck_id}; {comm}",
                           value=f"{color_rep} - {desc} ",
                           inline=False)


