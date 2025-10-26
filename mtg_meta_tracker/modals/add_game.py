import discord
from sqlalchemy import text, insert
from sqlalchemy.orm import Session
from ..sql import sql_try_insert_player, sql_insert_game_played
from ..db.models import Game, game_table

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

    def __init__(self, db_engine):
        super().__init__()
        self.engine = db_engine

    """
    NOTE - I'm worried that this will also 'time out' the modal, especially if cnx is going out to a remote server.
           I think the 'safest' thing to do will be to have all the DB stuff happen in scheduled background tasks.
           This would, similar to the decklist, get added to a queue that will be processed elsewhere. 
    """
    async def on_submit(self, interaction: discord.Interaction):

        with Session(self.engine) as session, session.begin():
            stmt = insert(game_table)
            res = session.execute(stmt, {'date': self.date.value, 'notes': self.notes.value})

            g_id = res.inserted_primary_key[0]
            for i, line in enumerate(self.players.value.split("\n")):
                    p, d = line.split(", ")
                    win = 1 if i == 0 else 0
                    print(p, d, win)

                    session.execute(text(sql_try_insert_player), {'idplayer': p})
                    session.execute(text(sql_insert_game_played), {
                        'idgame': g_id,
                        'idplayer': p,
                        'iddeck': d,
                        'winner': win
                    })

        await interaction.response.send_message(f'Added game record', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Error adding game.\n{error}', ephemeral=True)
