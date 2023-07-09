import discord
from discord.ext import commands
from decouple import config
import mysql.connector

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
cnx = mysql.connector.connect(user=config('DB_USER'), password=config('DB_PASSWORD'), host=config('DB_HOST'))

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

@bot.command()
async def mtt_add_deck(ctx, id_deck: str, id_color: str, desc: str):
    print(f"received: {id_deck}, {id_color}, {desc}")

    try:
        cur = cnx.cursor()
        cur.execute(sql_insert_deck, (id_deck, id_color, desc))
        cnx.commit()
        await ctx.send(f"added {id_deck}")
    except Exception as e:
        print(e)
        await ctx.send(f"error adding deck")

@bot.command()
async def mtt_add_game(ctx, p1, d1, p2, d2, p3, d3, p4, d4, date, note):
    cur = cnx.cursor()

    try:
        cur.execute(sql_insert_game, (date, note))
        g_id = cur.lastrowid

        for i, (p, d) in enumerate(zip([p1, p2, p3, p4], [d1, d2, d3, d4])):
            cur.execute(sql_try_insert_player, {'player': p})
            win = 1 if i == 0 else 0
            cur.execute(sql_insert_game_played, (g_id, p, d, win))

        cnx.commit()
        await ctx.send(f"added game played on {date}: {note}")
    except Exception as e:
        await ctx.send("error adding game.")

bot.run(config("DISCORD_BOT_TOKEN"))
