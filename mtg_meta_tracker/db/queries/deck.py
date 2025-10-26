from sqlalchemy import func, select, desc
from ..models import Deck, Game, GamePlayed, Player, Card, CardInDeck


def get_deck_wins(deck_id):
    return select(Deck.iddeck,
                  func.count(func.IF(GamePlayed.finish == 1, 1, None))) \
        .join(GamePlayed) \
        .where(Deck.iddeck == deck_id)


def get_deck(deck_id):
    return select(Deck.commander,
                  Deck.color,
                  Deck.desc) \
        .where(Deck.iddeck == deck_id)

sql_get_deck_cards = """
SELECT count, card.name, card.mana_cost, card.typeline, card.scryfall_uri FROM cards
JOIN card on card.oracle_id=cards.oracle_id
WHERE cards.iddeck=:iddeck
order by card.typeline, card.name asc;
"""

def get_deck_cards(deck_id):
    return select(CardInDeck.count,
                  Card.name,
                  Card.mana_cost,
                  Card.typeline,
                  Card.scryfall_uri) \
        .join(Card) \
        .where(CardInDeck.iddeck == deck_id)
