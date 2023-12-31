import discord
import nest_asyncio
nest_asyncio.apply()  # This allows the async's from the modal submit and the client card method to coexist.


class AddCards(discord.ui.Modal, title='Add Deck'):
    deck_id = discord.ui.TextInput(
        label='Deck ID',
        style=discord.TextStyle.short,
        placeholder='Deck ID of an existing deck.',
    )

    cards = discord.ui.TextInput(
        label='Card List',
        style=discord.TextStyle.long,
        placeholder="In '1 Cardname' format...",
        required=True,
    )

    def __init__(self):
        super().__init__(timeout=None)

    async def on_submit(self, interaction: discord.Interaction):
        card_list = []
        for line in self.cards.value.split('\n'):
            n, name = line.split(" ", 1)
            card_list.append((n, name))

        # We send the slightly-processed card list to the client, where a background task will
        # actually pull data from scryfall and add card data to the db and link it to a deck.
        interaction.client.add_deck_list_to_queue(card_list, self.deck_id.value, interaction.user.id)
        await interaction.response.send_message(f'Adding card list to queue for deck; {self.deck_id}.', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        if isinstance(error, ValueError):
            await interaction.response.send_message(f'Oops! Entries in the card list should look like: "1 CARDNAME"', ephemeral=True)
        else:
            await interaction.response.send_message(f'Oops! Something went wrong.\n{error}', ephemeral=True)
