import discord

from mtg_meta_tracker.app import MTTClient
from mtg_meta_tracker.modals import AddGame, AddDeck, AddCards
from mtg_meta_tracker.embeds import LBDeckEmbed, DeckSummaryEmbed, generate_card_list_embeds, GameRecordEmbed

from mtg_meta_tracker.views import AddGameMsg

def run(db_engine, discord_token, bot_channel_id):
    client = MTTClient(db_engine, bot_channel_id)

    @client.tree.command(description="Add a game record to the meta database.")
    async def add_game(interaction: discord.Interaction, seats: int, date: str, notes: str):
        await interaction.response.send_message(view=AddGameMsg(db_engine, seats, date, notes, interaction),
                                                embed=GameRecordEmbed([], date, notes))

    @client.tree.command(description="Add a deck to the database.")
    async def add_deck(interaction: discord.Interaction):
        await interaction.response.send_modal(AddDeck(db_engine))

    @client.tree.command(description="Add cards to a deck.")
    async def add_cards(interaction: discord.Interaction):
        await interaction.response.send_modal(AddCards())

    @client.tree.command(description="Show meta info for a given deck.")
    async def deck_summary(interaction: discord.Interaction, deck_id: str):
        meta_embed = DeckSummaryEmbed(f"Deck Summary - {deck_id}", db_engine, client.emojis, deck_id)
        await interaction.response.send_message(embed=meta_embed)

    @client.tree.command(description="Show cards for a given deck.")
    async def deck_cards(interaction: discord.Interaction, deck_id: str):
        card_embeds = generate_card_list_embeds(db_engine, client.emojis, deck_id)
        if len(card_embeds) == 0:
            await interaction.response.send_message(content="No cards in deck!")
        else:
            await interaction.response.send_message(embeds=card_embeds)

    @client.tree.command(description="Show the current leaderboard, by deck.")
    async def deck_lb(interaction: discord.Interaction):
        embed = LBDeckEmbed("Deck Leaderboard", db_engine, client.emojis)
        await interaction.response.send_message(embed=embed)

    client.run(discord_token)
