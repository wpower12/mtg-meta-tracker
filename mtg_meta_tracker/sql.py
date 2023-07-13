sql_insert_deck = """
INSERT INTO `mtg_meta_tracker`.`deck`
(`iddeck`, `color`, `desc`)
VALUES
(%s, %s, %s)
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