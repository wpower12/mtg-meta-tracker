import discord
from discord import app_commands

class MTTClient(discord.Client):
    def __init__(self) -> None:
        # Just default intents and a `discord.Client` instance
        # We don't need a `commands.Bot` instance because we are not
        # creating text-based commands.
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        # We need an `discord.app_commands.CommandTree` instance
        # to register application commands (slash commands in this case)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        # Sync the application command with Discord.
        await self.tree.sync()


