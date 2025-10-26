from sqlalchemy import func, select, desc
from ..models import Deck, Game, GamePlayed, Player


def player_summary(player_id):
    return select(func.count(func.IF(GamePlayed.finish == 1, 1, None)).label("wins"),
                  func.count().label("plays")) \
        .select_from(Player) \
        .join(GamePlayed) \
        .where(Player.idplayer == player_id)

def player_deck_summary(player_id):
    return select(Deck.iddeck,
                  Deck.color,
                  Deck.desc,
                  Deck.commander,
                  func.count(func.IF(GamePlayed.finish == 1, 1, None).label("wins")),
                  func.count().label("plays")) \
        .select_from(Player) \
        .join(Deck) \
        .join(GamePlayed) \
        .where(Player.idplayer == player_id) \
        .group_by(Deck.iddeck) \
        .order_by(desc(func.count(func.IF(GamePlayed.finish == 1, 1, None))))

