import mtg_meta_tracker
# import mysql.connector
import sqlalchemy
from decouple import config

# cnx = mysql.connector.connect(user=config('DB_USER'),
#                               password=config('DB_PASSWORD'),
#                               host=config('DB_HOST'), database="mtg_meta_tracker")
user = config('DB_USER')
pw   = config('DB_PASSWORD')
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{pw}@localhost/mtg_meta_tracker")

mtg_meta_tracker.run(engine, config("DISCORD_TEST_TOKEN"), config("BOT_CHANNEL_ID"))
