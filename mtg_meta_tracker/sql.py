sql_insert_deck = """
INSERT INTO `mtg_meta_tracker`.`deck`
(`iddeck`, `color`, `commander`, `desc`)
VALUES
(%s, %s, %s, %s)
"""

sql_try_insert_player = """
INSERT IGNORE INTO `mtg_meta_tracker`.`player`
(`idplayer`)
VALUES
(%(player)s)
"""

sql_insert_game = """
INSERT INTO `mtg_meta_tracker`.`game`
(`date`, `notes`)
VALUES
(%s, %s)
"""

sql_insert_game_played = """
INSERT INTO `mtg_meta_tracker`.`games_played`
(`idgame`, `idplayer`, `iddeck`, `winner`)
VALUES
(%s, %s, %s, %s)
"""

sql_deck_lb = """
SELECT deck.iddeck, deck.color, deck.desc, deck.commander, COUNT(*) as 'wins'
FROM games_played as gp
LEFT JOIN deck on gp.iddeck = deck.iddeck
WHERE winner=1
GROUP BY deck.iddeck
order by COUNT(*) DESC;
"""

sql_get_deck = """
SELECT commander, color, deck.desc FROM deck 
WHERE deck.iddeck=%s;
"""

sql_get_wins = """
SELECT count(*) as wins FROM deck 
JOIN games_played on games_played.iddeck=deck.iddeck
WHERE deck.iddeck=%s and winner=1
group by deck.iddeck;
"""

sql_get_deck_cards = """
SELECT count, card.name, card.mana_cost, card.typeline, card.scryfall_uri FROM cards
JOIN card on card.oracle_id=cards.oracle_id
WHERE cards.iddeck=%s
order by card.typeline, card.name asc;
"""

sql_insert_card = """
INSERT IGNORE INTO `mtg_meta_tracker`.`card`
(`oracle_id`, `scryfall_uri`, `cmc`, `color_identity`, `loyalty`, `mana_cost`, 
`name`, `oracle_text`,`power`,`power_numeric`,`toughness`,`toughness_numeric`,`typeline`)
VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

sql_insert_card_to_deck = """
INSERT IGNORE INTO `mtg_meta_tracker`.`cards`
(`oracle_id`, `iddeck`, `count`)
VALUES
(%s, %s, %s);
"""