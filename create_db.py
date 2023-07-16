from decouple import config
import mysql.connector

DB_NAME = "mtg_meta_tracker"

TABLES = [
    """CREATE TABLE `deck` (
      `iddeck` varchar(32) NOT NULL,
      `desc` mediumtext,
      `color` varchar(5) NOT NULL,
      `commander` varchar(45) NOT NULL, 
      PRIMARY KEY (`iddeck`)
    );""",
    """CREATE TABLE `game` (
      `idgame` int NOT NULL AUTO_INCREMENT,
      `date` datetime NOT NULL,
      `notes` mediumtext,
      PRIMARY KEY (`idgame`)
    );""",
    """CREATE TABLE `player` (
      `idplayer` varchar(64) NOT NULL,
      PRIMARY KEY (`idplayer`)
    );""",
    """CREATE TABLE `games_played` (
      `idgame` int NOT NULL,
      `idplayer` varchar(64) NOT NULL,
      `iddeck` varchar(32) NOT NULL,
      `winner` tinyint NOT NULL DEFAULT '0',
      PRIMARY KEY (`idgame`,`idplayer`,`iddeck`),
      KEY `fk_games_played_2_idx` (`idplayer`),
      KEY `fk_games_played_3_idx` (`iddeck`),
      CONSTRAINT `fk_games_played_1` FOREIGN KEY (`idgame`) REFERENCES `game` (`idgame`),
      CONSTRAINT `fk_games_played_2` FOREIGN KEY (`idplayer`) REFERENCES `player` (`idplayer`),
      CONSTRAINT `fk_games_played_3` FOREIGN KEY (`iddeck`) REFERENCES `deck` (`iddeck`)
    );""",
    """CREATE TABLE `card` (
      `oracle_id` varchar(255) NOT NULL,
      `scryfall_uri` text NOT NULL,
      `cmc` decimal(10,0) DEFAULT NULL,
      `color_identity` text,
      `color_indicator` text,
      `keywords` text,
      `loyalty` text,
      `mana_cost` text,
      `name` text NOT NULL,
      `oracle_text` text,
      `power` text,
      `power_numeric` int DEFAULT NULL,
      `produced_mana` text,
      `toughness` text,
      `toughness_numeric` int DEFAULT NULL,
      `typeline` text,
      PRIMARY KEY (`oracle_id`),
      KEY `num_power` (`power_numeric`),
      KEY `num_toughness` (`toughness_numeric`),
      KEY `num_cmc` (`cmc`),
      FULLTEXT KEY `ft_keywords` (`keywords`),
      FULLTEXT KEY `ft_mana_cost` (`mana_cost`),
      FULLTEXT KEY `ft_name` (`name`),
      FULLTEXT KEY `ft_oracle_text` (`oracle_text`),
      FULLTEXT KEY `ft_power` (`power`),
      FULLTEXT KEY `ft_toughness` (`toughness`),
      FULLTEXT KEY `ft_typeline` (`typeline`),
      FULLTEXT KEY `ft_color_identity` (`color_identity`),
      FULLTEXT KEY `ft_color_indicator` (`color_indicator`)
    ); """,
    """CREATE TABLE `cards` (
      `oracle_id` varchar(255) NOT NULL,
      `iddeck` varchar(32) NOT NULL,
      `count` int NOT NULL DEFAULT '1',
      PRIMARY KEY (`oracle_id`,`iddeck`)
    );"""
]

cnx = mysql.connector.connect(user=config('DB_USER'), password=config('DB_PASSWORD'), host=config('DB_HOST'))
cur = cnx.cursor()

cur.execute(f"CREATE DATABASE {DB_NAME};")
cnx.commit()

cur.execute(f"USE {DB_NAME};")
cnx.commit()

for TABLE in TABLES:
    cur.execute(TABLE)
cnx.commit()
