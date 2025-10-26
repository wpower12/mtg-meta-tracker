from sqlalchemy import Date, String, Text, Table, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import registry

mapper_registry = registry()

player_table = Table(
    "player",
    mapper_registry.metadata,
    Column("idplayer", String(64), primary_key=True)
)

league_table = Table(
    "league",
    mapper_registry.metadata,
    Column("idleague", String(64), primary_key=True, nullable=False),
    Column("date_created", Date, nullable=False),
    Column("notes", Text)
)

deck_table = Table(
    "deck",
    mapper_registry.metadata,
    Column("iddeck", String(64), primary_key=True),
    Column("creator", String(64), ForeignKey("player.idplayer"), nullable=False),
    Column("desc", Text),
    Column("color", Text),
    Column("commander", Text)
)

game_table = Table(
    "game",
    mapper_registry.metadata,
    Column("idgame", Integer, primary_key=True),
    Column("date", Date),
    Column("format", Text),
    Column("league", String(64), ForeignKey("league.idleague")),
    Column("notes", Text)
)

card_table = Table(
    "card",
    mapper_registry.metadata,
    Column("oracle_id", String(64), primary_key=True),
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

games_played_table = Table(
    "games_played",
    mapper_registry.metadata,
    Column("idgame", Integer, ForeignKey("game.idgame"), primary_key=True),
    Column("idplayer", String(64), ForeignKey("player.idplayer"), primary_key=True),
    Column("iddeck", String(64), ForeignKey("deck.iddeck"), primary_key=True),
    Column("finish", Integer, nullable=False),
    Column("points", Integer),
    Column("point_notes", Text)
)

cards_table = Table(
    "cards",
    mapper_registry.metadata,
    Column("oracle_id", String(64), ForeignKey("card.oracle_id"), primary_key=True),
    Column("iddeck", String(64), ForeignKey("deck.iddeck"), primary_key=True),
    Column("count", Integer)
)

class Game:
    pass

class Card:
    pass

class Deck:
    pass

class Player:
    pass

class League:
    pass

class CardInDeck:
    pass

class GamePlayed:
    pass


mapper_registry.map_imperatively(Player, player_table)
mapper_registry.map_imperatively(Deck, deck_table)
mapper_registry.map_imperatively(League, league_table)
mapper_registry.map_imperatively(Game, game_table)
mapper_registry.map_imperatively(Card, card_table)
mapper_registry.map_imperatively(CardInDeck, cards_table)
mapper_registry.map_imperatively(GamePlayed, games_played_table)
