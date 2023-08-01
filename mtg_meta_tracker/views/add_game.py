import discord

from sqlalchemy import insert, text
from sqlalchemy.orm import Session

from ..embeds import GameRecordEmbed
from ..sql import sql_get_players, sql_get_decks, sql_try_insert_player, sql_insert_game_played
from ..models import game_table


class AddPlayerMsg(discord.ui.View):
    def __init__(self, db_engine, n, addgame_msg):
        super(AddPlayerMsg, self).__init__()
        self.n = n
        self.ag_msg = addgame_msg

        with Session(db_engine) as session:
            res = session.execute(text(sql_get_players))
            players = res.fetchall()
            res = session.execute(text(sql_get_decks))
            decks = res.fetchall()

        player_options = [discord.SelectOption(label=f"{p[0]}") for p in players]
        deck_options   = [discord.SelectOption(label=f"{d[0]}") for d in decks]

        player_select = discord.ui.Select(placeholder="Select Player", options=player_options)
        player_select.callback = self.select_player
        deck_select = discord.ui.Select(placeholder="Select Deck", options=deck_options)
        deck_select.callback = self.select_deck

        self.add_item(player_select)
        self.add_item(deck_select)

        self.player_select = player_select
        self.deck_select = deck_select

        self.player = None
        self.deck = None

    async def select_player(self, interaction: discord.Interaction):
        await interaction.response.defer()

    async def select_deck(self, interaction: discord.Interaction):
        await interaction.response.defer()

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green, row=4)
    async def add_deck(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.style = discord.ButtonStyle.gray
        button.disabled = True
        player = self.player_select.values[0]
        deck   = self.deck_select.values[0]
        await self.ag_msg.add_player(player, deck, self.n)
        await interaction.response.edit_message(content=f"Added player, deck to game", view=self)
        await interaction.delete_original_response()

class DynButton(discord.ui.Button):
    def __init__(self, label, n, parent_msg, *args, **kwargs):
        super(DynButton, self).__init__(label=label, *args, **kwargs)
        self.style = discord.ButtonStyle.green
        self.parent = parent_msg
        self.n = n

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=AddPlayerMsg(self.parent.db, self.n, self.parent))


PLACE_STRS = ["1st", "2nd", "3rd", "4th"]

class AddGameMsg(discord.ui.View):
    def __init__(self, cnx, seats, date, notes, interaction):
        super(AddGameMsg, self).__init__()

        self.db = cnx
        self.interaction = interaction
        self.buttons = [DynButton(f"{PLACE_STRS[i]}", i, self) for i in range(seats)]
        self.player_data = [None for _ in range(seats)]
        self.players = seats
        self.date = date
        self.notes = notes

        for btn in self.buttons:
            self.add_item(btn)

        self.sub_button = discord.ui.Button(disabled=True, label="Submit")
        self.sub_button.callback = self.submit_record
        self.add_item(self.sub_button)

    async def add_player(self, p, d, n):
        self.player_data[n] = [p, d]
        self.players -= 1
        if self.players <= 0:
            self.sub_button.disabled = False
            self.sub_button.style = discord.ButtonStyle.green
        gr_embed = GameRecordEmbed(self.player_data, self.date, self.notes)
        msg = await self.interaction.original_response()
        await msg.edit(view=self, embed=gr_embed)

    async def submit_record(self, interaction: discord.Interaction):
        await interaction.response.defer()

        for btn in self.buttons:
            self.remove_item(btn)
        self.remove_item(self.sub_button)

        with Session(self.db) as session, session.begin():
            stmt = insert(game_table)
            res = session.execute(stmt, {'date': self.date, 'notes': self.notes})
            g_id = res.inserted_primary_key[0]
            for i, [p, d] in enumerate(self.player_data):
                win = 1 if i == 0 else 0

                session.execute(text(sql_try_insert_player), {'idplayer': p})
                session.execute(text(sql_insert_game_played), {
                    'idgame': g_id,
                    'idplayer': p,
                    'iddeck': d,
                    'winner': win
                })

        gr_embed = GameRecordEmbed(self.player_data, self.date, self.notes)
        msg = await self.interaction.original_response()
        await msg.edit(view=self, embed=gr_embed)
