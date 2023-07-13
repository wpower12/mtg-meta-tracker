import discord
from ..sql import sql_try_insert_player, sql_insert_game, sql_insert_game_played

class AddGame(discord.ui.Modal, title='Add Game'):
    date = discord.ui.TextInput(
        label='Date',
        style=discord.TextStyle.short,
        placeholder='In YYYY-MM-DD ...',
    )

    players = discord.ui.TextInput(
        label='Players',
        style=discord.TextStyle.long,
        placeholder="One per line, winner first; USERNAME, DECKID",
        required=True,
        max_length=300,
    )

    notes = discord.ui.TextInput(
        label="Notes",
        style=discord.TextStyle.long,
        placeholder='Type game notes here...',
        required=False,
        max_length=300,
    )

    def __init__(self, cnx):
        super().__init__()
        self.db = cnx

    async def on_submit(self, interaction: discord.Interaction):
        cur = self.db.cursor()
        try:
            cur.execute(sql_insert_game, (self.date.value, self.notes.value))
            g_id = cur.lastrowid
            for i, line in enumerate(self.players.value.split("\n")):
                p, d = line.split(", ")
                win = 1 if i == 0 else 0
                print(p, d, win)
                cur.execute(sql_try_insert_player, {'player': p})
                cur.execute(sql_insert_game_played, (g_id, p, d, win))
            self.db.commit()
        except Exception as e:
            raise e

        await interaction.response.send_message(f'Added game record', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong.\n{error}', ephemeral=True)

"""
Powpowpow, AUNTIE
Dr. Nicky, DARKELVES
Chucky, URZA_ARTS
Paul, WHITE_RABBIT
"""