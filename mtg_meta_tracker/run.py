import discord

from mtg_meta_tracker.app import MTTClient
# from mtg_meta_tracker.modals import AddGame, AddDeck, AddCards
from mtg_meta_tracker.modals import AddDeck, AddCards
from mtg_meta_tracker.views import AddGameMsg
from mtg_meta_tracker.embeds import LBDeckEmbed, DeckSummaryEmbed, generate_card_list_embeds

def run(db_cnx, discord_token):
    client = MTTClient(db_cnx)

    @client.tree.command(description="Add a game record to the meta database.")
    async def add_game(interaction: discord.Interaction):
        await interaction.response.send_modal(AddGame(db_cnx))

    @client.tree.command(description="Add a deck to the database.")
    async def add_deck(interaction: discord.Interaction):
        await interaction.response.send_modal(AddDeck(db_cnx))

    @client.tree.command(description="Add cards to a deck.")
    async def add_cards(interaction: discord.Interaction):
        await interaction.response.send_modal(AddCards())

    @client.tree.command(description="Show meta info for a given deck.")
    async def deck_summary(interaction: discord.Interaction, deck_id: str):
        meta_embed = DeckSummaryEmbed(f"Deck Summary - {deck_id}", db_cnx, client.emojis, deck_id)
        await interaction.response.send_message(embed=meta_embed)

    @client.tree.command(description="Show cards for a given deck.")
    async def deck_cards(interaction: discord.Interaction, deck_id: str):
        card_embeds = generate_card_list_embeds(db_cnx, client.emojis, deck_id)
        await interaction.response.send_message(embeds=card_embeds)

    @client.tree.command(description="Show the current leaderboard, by deck.")
    async def deck_lb(interaction: discord.Interaction):
        embed = LBDeckEmbed("Deck Leaderboard", db_cnx, client.emojis)
        await interaction.response.send_message(embed=embed)

    client.run(discord_token)
