import discord
from sqlalchemy import text, insert
from sqlalchemy.orm import Session

from ..db.models import deck_table, player_table


class AddDeck(discord.ui.Modal, title='Add Deck'):
    deck_id = discord.ui.TextInput(
        label='Deck ID',
        style=discord.TextStyle.short,
        placeholder='Short name for the deck, will be used to add it to games.',
    )

    colors = discord.ui.TextInput(
        label='Color ID',
        style=discord.TextStyle.short,
        placeholder="Using WUBRG ...",
        required=True,
    )

    comm = discord.ui.TextInput(
        label='Commander',
        style=discord.TextStyle.short,
        placeholder="",
        required=True,
    )

    desc = discord.ui.TextInput(
        label="Description",
        style=discord.TextStyle.long,
        placeholder='Short description of the deck.',
        required=True,
        max_length=140,
    )

    decklist_url = discord.ui.TextInput(
        label='Decklist URL',
        style=discord.TextStyle.short,
        placeholder="Moxfield, goldfish, w.e..",
        required=False,
    )

    def __init__(self, db_engine):
        super().__init__()
        self.engine = db_engine

    async def on_submit(self, interaction: discord.Interaction):
        with Session(self.engine) as session, session.begin():
            deck_data = {
                'iddeck': self.deck_id.value,
                'color': self.colors.value,
                'commander': self.comm.value,
                'desc': self.desc.value,
                'creator': interaction.user.display_name
            }
            session.execute(insert(player_table), {'idplayer': interaction.user.display_name})
            session.execute(insert(deck_table), deck_data)

        await interaction.response.send_message(f'Added Deck; {self.deck_id}', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong.\n{error}', ephemeral=True)
