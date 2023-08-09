sql_insert_deck = """
INSERT INTO `mtg_meta_tracker`.`deck`
(`iddeck`, `color`, `commander`, `desc`, `creator`)
VALUES
(:iddeck, :color, :commander, :desc, :creator)
"""

sql_try_insert_player = """
INSERT IGNORE INTO `mtg_meta_tracker`.`player`
(`idplayer`)
VALUES
(:idplayer)
"""

sql_insert_game = """
INSERT INTO `mtg_meta_tracker`.`game`
(`date`, `notes`)
VALUES
(:date, :notes)
"""

sql_insert_game_played = """
INSERT INTO `mtg_meta_tracker`.`games_played`
(`idgame`, `idplayer`, `iddeck`, `winner`)
VALUES
(:idgame, :idplayer, :iddeck, :winner)
"""

sql_deck_lb = """
SELECT 
    deck.iddeck, deck.color, deck.desc, deck.commander, 
    COUNT(IF(gp.winner=1, 1, Null)) as 'wins', COUNT(*) as 'plays'
FROM games_played as gp
LEFT JOIN deck on gp.iddeck = deck.iddeck
GROUP BY deck.iddeck
order by COUNT(IF(gp.winner=1, 1, Null)) DESC;
"""

sql_user_lb = """
SELECT player.idplayer, COUNT(IF(games_played.winner=1, 1, Null)) as 'wins', COUNT(*) as 'plays' FROM player
LEFT JOIN games_played ON games_played.idplayer=player.idplayer
GROUP BY player.idplayer
order by COUNT(IF(games_played.winner=1, 1, Null)) DESC;
"""

sql_get_deck = """
SELECT commander, color, deck.desc FROM deck 
WHERE deck.iddeck=:iddeck;
"""

sql_get_wins = """
SELECT count(*) as wins FROM deck 
JOIN games_played on games_played.iddeck=deck.iddeck
WHERE deck.iddeck=:iddeck and winner=1
group by deck.iddeck;
"""

sql_get_deck_cards = """
SELECT count, card.name, card.mana_cost, card.typeline, card.scryfall_uri FROM cards
JOIN card on card.oracle_id=cards.oracle_id
WHERE cards.iddeck=:iddeck
order by card.typeline, card.name asc;
"""

sql_insert_card = """
INSERT IGNORE INTO `mtg_meta_tracker`.`card`
(`oracle_id`, `scryfall_uri`, `cmc`, `color_identity`, `loyalty`, `mana_cost`, 
`name`, `oracle_text`,`power`,`power_numeric`,`toughness`,`toughness_numeric`,`typeline`)
VALUES
(:oracle_id, :scryfall_uri, :cmc, :color, :loyalty, :mana_cost, :name, :oracle_text, 
:power, :power_num, :tough, :tough_num, :type_line);
"""

sql_insert_card_to_deck = """
INSERT IGNORE INTO `mtg_meta_tracker`.`cards`
(`oracle_id`, `iddeck`, `count`)
VALUES
(:oracle_id, :iddeck, :count);
"""

sql_get_players = """SELECT idplayer FROM mtg_meta_tracker.player;"""

sql_get_decks = """SELECT iddeck FROM mtg_meta_tracker.deck;"""

sql_get_user_summary = """
SELECT COUNT(IF(games_played.winner=1, 1, Null)) as 'wins', COUNT(*) as 'plays' FROM player
LEFT JOIN games_played ON games_played.idplayer=player.idplayer
WHERE player.idplayer=:idplayer
GROUP BY player.idplayer
"""

sql_get_user_deck_summary = """
SELECT deck.iddeck, deck.commander, deck.desc, deck.color, COUNT(IF(gp.winner=1, 1, NULL)) as 'wins', COUNT(*) as 'plays'
FROM player 
JOIN deck on deck.creator=player.idplayer
JOIN games_played as gp on gp.iddeck=deck.iddeck
WHERE player.idplayer=:idplayer
GROUP BY deck.iddeck, deck.desc, deck.color;
"""