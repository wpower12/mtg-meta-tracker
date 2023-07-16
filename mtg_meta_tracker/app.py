import discord
from discord.ext import tasks
from discord import app_commands

import scrython
import time

from .sql import sql_insert_card, sql_insert_card_to_deck

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
        # Sync the application command with Discord.
        self.add_available_deck_lists.start()
        await self.tree.sync()

    @tasks.loop(seconds=2)
    async def add_available_deck_lists(self):
        if len(self.deck_lists) > 0:
            cur = self.cnx.cursor()
            deck_id, deck_list = self.deck_lists.pop()
            for n, name in deck_list:
                card = scrython.cards.Named(fuzzy=name)

                # TODO - Do this in literally any other way.
                try:
                    power = card.power()
                    tough = card.toughness()
                except KeyError:
                    power = None
                    tough = None

                try:
                    num_pow = float(card.power())
                except ValueError:
                    num_pow = None
                except KeyError:
                    num_pow = None

                try:
                    num_tou = float(card.toughness())
                except ValueError:
                    num_tou = None
                except KeyError:
                    num_tou = None

                try:
                    loyalty = card.loyalty()
                except KeyError:
                    loyalty = ""

                color_id_str = "".join(card.color_identity())

                # print(n, name, card)
                card_insert_data = (
                    card.oracle_id(),
                    card.scryfall_uri(),
                    card.cmc(),
                    color_id_str,
                    loyalty,
                    card.mana_cost(),
                    card.name(),
                    card.oracle_text(),
                    power,
                    num_pow,
                    tough,
                    num_tou,
                    card.type_line())

                # Insert the CARD
                cur.execute(sql_insert_card, card_insert_data)
                cur.execute(sql_insert_card_to_deck, (card.oracle_id(), deck_id, n))

                # print(card_insert_data)
                time.sleep(0.1)

            self.cnx.commit()

