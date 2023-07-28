sql_insert_deck = """
INSERT INTO `mtg_meta_tracker`.`deck`
(`iddeck`, `color`, `commander`, `desc`)
VALUES
(:iddeck, :color, :commander, :desc)
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
SELECT deck.iddeck, deck.color, deck.desc, deck.commander, COUNT(*) as 'wins'
FROM games_played as gp
LEFT JOIN deck on gp.iddeck = deck.iddeck
WHERE winner=1
GROUP BY deck.iddeck
order by COUNT(*) DESC;
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