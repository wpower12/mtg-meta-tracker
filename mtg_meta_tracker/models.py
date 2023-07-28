from sqlalchemy import Date, Text, Table, Column, Integer, Float
from sqlalchemy.orm import registry

mapper_registry = registry()

game_table = Table(
    "game",
    mapper_registry.metadata,
    Column("idgame", Integer, primary_key=True),
    Column("date", Date),
    Column("notes", Text)
)

card_table = Table(
    "card",
    mapper_registry.metadata,
    Column("oracle_id", Text, primary_key=True),
    Column("scryfall_uri", Text),
    Column("cmc", Float),
    Column("color_identity", Text),
    Column("color_indicator", Text),
    Column("keywords", Text),
    Column("loyalty", Text),
    Column("mana_cost", Text),
    Column("name", Text),
    Column("oracle_text", Text),
    Column("power", Text),
    Column("toughness", Text),
    Column("produced_mana", Text),
    Column("typeline", Text),
    Column("power_numeric", Integer),
    Column("toughness_numeric", Integer),
)

class Game:
    pass

class Card:
    pass


mapper_registry.map_imperatively(Game, game_table)
mapper_registry.map_imperatively(Card, card_table)
