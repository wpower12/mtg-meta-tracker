import discord
from discord.ext import tasks
from discord import app_commands

from sqlalchemy import insert, text
from sqlalchemy.orm import Session

import scrython
import time

from .sql import sql_insert_card_to_deck
from .util import parse_scryfalljson
from .models import card_table


class MTTClient(discord.Client):
    def __init__(self, db_engine, bot_channel_id) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.engine = db_engine
        self.channel_id = bot_channel_id

        self.tree = app_commands.CommandTree(self)
        self.deck_lists = []

    def add_deck_list_to_queue(self, dl, deck_id):
        self.deck_lists.append([deck_id, dl])

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def setup_hook(self) -> None:
        self.add_available_deck_lists.start()
        await self.tree.sync()

    @tasks.loop(seconds=2)
    async def add_available_deck_lists(self):
        if len(self.deck_lists) > 0:
            err_cards, success_cards = [], []
            deck_id, deck_list = self.deck_lists.pop()
            for n, name in deck_list:
                with Session(self.engine) as session, session.begin():
                    try:
                        card = scrython.cards.Named(fuzzy=name, format='json')
                        card_insert_data = parse_scryfalljson(card.scryfallJson)
                        stmt = insert(card_table).prefix_with('IGNORE')
                        session.execute(stmt, card_insert_data)
                        session.execute(text(sql_insert_card_to_deck),
                                        {"oracle_id": card.oracle_id(),
                                         "iddeck": deck_id,
                                         "count": n})
                        success_cards.append(name)
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"error adding {name}")
                        print(e)
                        err_cards.append(name)

            # if len(success_cards) > 0:
            #     suc_cards_str = "\n".join(success_cards)
            #     channel = self.get_channel(self.channel_id)
            #     await channel.send(content=f"Successfully added cards to {deck_id}:\n{suc_cards_str}")
            # if len(err_cards) > 0:
            #     err_cards_str = "\n".join(err_cards)
            #     channel = self.get_channel(self.channel_id)
            #     await channel.send(content=f"Error adding cards to {deck_id}:\n{err_cards_str}")
