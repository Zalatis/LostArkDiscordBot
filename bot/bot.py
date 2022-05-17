from glob import glob
from datetime import datetime
import discord
from discord.ext import commands
from discord import ui
import os,json
from pathlib import Path
from pytz import timezone
from .database.db_setup import Database

# Bot subclass
class BotSubclass(commands.Bot):

    def __init__(self):

        config_path = "config.json"
        if os.path.exists('debugconfig.json'): # Use configurations for test server
            config_path = 'debugconfig.json'

        # Get Tokens and global variables
        with open(config_path, "r", encoding='utf8') as config:
            self._DATA = json.load(config)

            for x in self._DATA:
                if x == "TIMEZONE":
                    self.TIMEZONE = timezone(self._DATA[x])
                elif "CHANNEL_ID" in x:
                    setattr(self, x, int(self._DATA[x]))
                elif "MONGO_URI" in x:
                    self.db = Database(self._DATA['MONGO_URI'])
                else:
                    setattr(self, x, self._DATA[x])

        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        self._intents = discord.Intents().all()

        super().__init__(command_prefix=self.prefix, intents = self._intents, case_insensitive=True)
        self.setup()


    #Bot login,logout and setup

    def setup(self):

        print("Starting to load cogs...")
        for cog in self._cogs:
            try:
                self.load_extension(f"bot.cogs.{cog}")
                print(f"Extension {cog} loaded.")
            except Exception as exc:
                print(f"Failed to load extension {cog}: {exc}")
                raise exc
        print('Completed loading cogs')

    def run(self):

        print('Running Bot')
        super().run(self.BOT_TOKEN)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
            print("Closing on keyboard interrupt...")
            for vc in self.voice_clients:
                if hasattr(vc,"cleanup_and_disconnect"):
                    await vc.cleanup_and_disconnect()
                else:
                    await vc.disconnect()
            await super().close()
            await self.shutdown()

    async def on_connect(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time, f"- Connecté à Discord (latence: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time, "- Bot reconnecté.")

    async def on_disconnect(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time, "- Bot déconnecté.")

    async def on_ready(self):

        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = "farmers"))
        
        # Force le chargement des commandes
        await self.sync_commands(force=True)
        await self.register_commands(force=True)

        self.guild = await self.fetch_guild(self.GUILD_ID)

        # await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{self.PREFIX}help"))
        # await self.change_presence(status=discord.Activity(type=discord.ActivityType.watching, name = "farming"))
        print(discord.__version__)

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(self.BOT_PREFIX)(bot, msg)


    
