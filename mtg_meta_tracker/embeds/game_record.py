import discord

PLACE_STRS = ["1st", "2nd", "3rd", "4th"]

class GameRecordEmbed(discord.Embed):

    def __init__(self, player_data, date, notes):
        super(GameRecordEmbed, self).__init__(title="Game Record")

        self.add_field(name=date, value=notes, inline=False)
        for n, pd in enumerate(player_data):
            if pd is not None:
                p, d = pd
                self.add_field(name=f"{PLACE_STRS[n]}", value=f"{p} - {d}")



