import discord
from ..sql import sql_insert_deck


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

    def __init__(self, cnx):
        super().__init__()
        self.db = cnx

    async def on_submit(self, interaction: discord.Interaction):
        cur = self.db.cursor()
        try:
            cur.execute(sql_insert_deck, (self.deck_id.value, self.colors.value, self.comm.value, self.desc.value))
        except Exception as e:
            raise e

        await interaction.response.send_message(f'Added Deck; {self.deck_id}', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong.\n{error}', ephemeral=True)
