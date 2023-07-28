import mtg_meta_tracker
# import mysql.connector
import sqlalchemy
from decouple import config

user = config('DB_USER')
pw   = config('DB_PASSWORD')
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{pw}@localhost/mtg_meta_tracker")

mtg_meta_tracker.run(engine, config("DISCORD_TEST_TOKEN"), config("BOT_CHANNEL_ID"))
