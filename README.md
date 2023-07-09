# mtg-meta-tracker
Start of a bot to track commander games played via a discord bot.

This assumes you have a working mysql server running, and have a .env file in the root of this project directory that contains the following:

```
DISCORD_BOT_TOKEN=<YOUR TOKEN>
DB_USER="<YOUR UN>"
DB_PASSWORD="<YOUR PW>"
DB_HOST="localhost"
```

The create_db.py script should be able to generate the necessary tables and such, but it's not very tested, sooo my b.