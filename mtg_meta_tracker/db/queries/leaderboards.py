from sqlalchemy import func, select, desc
from ..models import Deck, Game, GamePlayed, Player


def deck_leaderboard_overall(limit=5):
    return select(Deck.iddeck,
                  Deck.color,
                  Deck.desc,
                  Deck.commander,
                  func.count(func.IF(GamePlayed.finish == 1, 1, None).label("wins")),
                  func.count().label("plays")) \
        .join(Deck) \
        .group_by(Deck.iddeck) \
        .order_by(desc(func.count(func.IF(GamePlayed.finish == 1, 1, None)))) \
        .limit(limit)

def user_leaderboard_overall(limit=5):
    return select(Player.idplayer,
                  func.count(func.IF(GamePlayed.finish == 1, 1, None)).label("wins"),
                  func.count().label("plays")) \
        .join(GamePlayed) \
        .group_by(Player.idplayer) \
        .order_by(desc(func.count(func.IF(GamePlayed.finish == 1, 1, None)))) \
        .limit(limit)

def user_leaderboard_per_league(league_id, limit=5):
    return select(Player.idplayer,
                  func.sum(GamePlayed.points).label("points"),
                  func.count(func.IF(GamePlayed.finish == 1, 1, None)).label("wins"),
                  func.count().label("plays")) \
        .join(GamePlayed) \
        .join(Game) \
        .where(Game.league == league_id) \
        .group_by(Player.idplayer) \
        .order_by(desc(func.sum(GamePlayed.points))) \
        .limit(limit)
