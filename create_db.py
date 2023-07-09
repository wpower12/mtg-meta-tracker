from decouple import config
import mysql.connector

DB_NAME = "mtg_meta_tracker"

CREATE_TABLES = """
    CREATE TABLE `deck` (
      `iddeck` varchar(32) NOT NULL,
      `desc` mediumtext,
      `color` varchar(5) NOT NULL,
      PRIMARY KEY (`iddeck`)
    );
    CREATE TABLE `game` (
      `idgame` int NOT NULL AUTO_INCREMENT,
      `date` datetime NOT NULL,
      `notes` mediumtext,
      PRIMARY KEY (`idgame`)
    );
    CREATE TABLE `player` (
      `idplayer` varchar(64) NOT NULL,
      PRIMARY KEY (`idplayer`)
    );
    CREATE TABLE `games_played` (
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
    );
"""

cnx = mysql.connector.connect(user=config('DB_USER'), password=config('DB_PASSWORD'), host=config('DB_HOST'))
cur = cnx.cursor()

cur.execute(f"CREATE DATABSE {DB_NAME};")
cur.execute(f"USE {DB_NAME};")
cur.execute(CREATE_TABLES)
cnx.commit()
