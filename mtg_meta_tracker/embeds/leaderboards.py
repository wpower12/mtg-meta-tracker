import discord
from sqlalchemy.orm import Session
from ..db.queries.leaderboards import deck_leaderboard_overall, user_leaderboard_overall

class LBDeckEmbed(discord.Embed):

    def __init__(self, title, db_engine):
        super(LBDeckEmbed, self).__init__(title=title)

        with Session(db_engine) as session:
            res = session.execute(deck_leaderboard_overall())
            decks = res.fetchall()

        for (deck_id, color, desc, comm, wins, plays) in decks:
            if wins == 1:
                win_str = "win"
            else:
                win_str = "wins"
            self.add_field(name=f"{wins} {win_str}, {plays} plays: {deck_id}",
                           value=f"{comm} - {desc}",
                           inline=False)

class LBUserEmbed(discord.Embed):

    def __init__(self, title, db_engine):
        super(LBUserEmbed, self).__init__(title=title)

        with Session(db_engine) as session:
            res = session.execute(user_leaderboard_overall())
            user_records = res.fetchall()

        for (user, wins, played) in user_records:
            if wins == 1:
                win_str = "win"
            else:
                win_str = "wins"
            self.add_field(name="", value=f"{user} - {wins} {win_str}, {played} played",
                           inline=False)
