import discord
from decouple import config
import mysql.connector
from discord.utils import get

from mtg_meta_tracker.app import MTTClient
from mtg_meta_tracker.modals import AddGame, AddDeck
from mtg_meta_tracker.sql import sql_deck_lb

client = MTTClient()
cnx = mysql.connector.connect(user=config('DB_USER'),
                              password=config('DB_PASSWORD'),
                              host=config('DB_HOST'), database="mtg_meta_tracker")

@client.tree.command(description="Add a game record to the meta database.")
async def add_game(interaction: discord.Interaction):
    await interaction.response.send_modal(AddGame(cnx))

@client.tree.command(description="Add a deck to the database.")
async def add_deck(interaction: discord.Interaction):
    await interaction.response.send_modal(AddDeck(cnx))

@client.tree.command(description="Show the current leaderboard, by deck.")
async def deck_lb(interaction: discord.Interaction):
    cur = cnx.cursor()
    cur.execute(sql_deck_lb)
    embed = discord.Embed(title="Deck Leaderboard")
    for (deck_id, color, desc, comm, wins) in cur:
        color_rep = ""
        for c in color:
            mana_em_name = f"mana{c.lower()}"
            color_rep += str(get(client.emojis, name=mana_em_name))

        if wins == 1:
            win_str = "win"
        else:
            win_str = "wins"

        embed.add_field(name=f"{wins} {win_str}: {deck_id}; {comm}", value=f"{color_rep} - {desc} ", inline=False)
    await interaction.response.send_message(embed=embed)

client.run(config("DISCORD_BOT_TOKEN"))
