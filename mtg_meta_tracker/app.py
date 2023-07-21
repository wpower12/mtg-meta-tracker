import discord
from discord.ext import tasks
from discord import app_commands

import scrython
import time

from .sql import sql_insert_card, sql_insert_card_to_deck
from .util import parse_scryfalljson

class MTTClient(discord.Client):
    def __init__(self, db) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.cnx = db
        self.tree = app_commands.CommandTree(self)
        self.deck_lists = []

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        self.add_available_deck_lists.start()
        await self.tree.sync()

    @tasks.loop(seconds=2)
    async def add_available_deck_lists(self):
        if len(self.deck_lists) > 0:

            with self.cnx.cursor() as cur:
                deck_id, deck_list = self.deck_lists.pop()

                for n, name in deck_list:
                    try:
                        card = scrython.cards.Named(fuzzy=name, format='json')
                        card_insert_data = parse_scryfalljson(card.scryfallJson)
                        cur.execute(sql_insert_card, card_insert_data)
                        cur.execute(sql_insert_card_to_deck, (card.oracle_id(), deck_id, n))
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"error adding {name}")
                        print(e)

                self.cnx.commit()
