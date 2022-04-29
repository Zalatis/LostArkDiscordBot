from glob import glob
from datetime import datetime
import discord
from discord.ext import commands
from discord import ui
import os,json
from pathlib import Path
from pytz import timezone

# Bot subclass
class BotSubclass(commands.Bot):

    def __init__(self):

        config_path = "config.json"
        if os.path.exists('debugconfig.json'): # Use configurations for test server
            config_path = 'debugconfig.json'

        # Get Tokens and global variables
        with open(config_path, "r") as config:
            self._DATA = json.load(config)

            self._TOKEN = self._DATA["BOT_TOKEN"]
            self.PREFIX = self._DATA["BOT_PREFIX"]
            self.DEV_ID = self._DATA['DEV_ID']
            self.PERMITED_ROLES_IDS = self._DATA['PERMITED_ROLES_IDS']
            self.BOT_ID = self._DATA['BOT_ID']

            self.TIMEZONE = timezone(self._DATA['TIMEZONE'])

            self.GUILD_ID = self._DATA['GUILD_ID']

            self.MARCHAND_CHANNEL_ID = int(self._DATA['MARCHAND_CHANNEL_ID'])
            self.HEBDO_CHOICE_CHANNEL_ID = self._DATA['HEBDO_CHOICE_CHANNEL_ID']
            self.NEWS_CHANNEL_ID = self._DATA['NEWS_CHANNEL_ID']
            self.ROLES_CHANNEL_ID = self._DATA['ROLES_CHANNEL_ID']
            self.RESSOURCES_CHANNEL_ID = self._DATA['RESSOURCES_CHANNEL_ID']
            self.RAPPEL_CHANNEL_ID = self._DATA['RAPPEL_CHANNEL_ID']

            self.SPOTIFY_ID = self._DATA['SPOTIFY_ID']
            self.SPOTIFY_SECRET = self._DATA['SPOTIFY_SECRET']


            self.PISTOLANCIER_ROLE_ID = self._DATA['PISTOLANCIER_ROLE_ID']
            self.DESTRUCTEUR_ROLE_ID = self._DATA['DESTRUCTEUR_ROLE_ID']
            self.BERSERKER_ROLE_ID = self._DATA['BERSERKER_ROLE_ID']
            self.PALADIN_ROLE_ID = self._DATA['PALADIN_ROLE_ID']
            self.ELEMENTISTE_ROLE_ID = self._DATA['ELEMENTISTE_ROLE_ID']
            self.ESSENTIALISTE_ROLE_ID = self._DATA['ESSENTIALISTE_ROLE_ID']
            self.SPIRITE_ROLE_ID = self._DATA['SPIRITE_ROLE_ID']
            self.PUGILISTE_ROLE_ID = self._DATA['PUGILISTE_ROLE_ID']
            self.LANCIERE_ROLE_ID = self._DATA['LANCIERE_ROLE_ID']
            self.FRANCTIREUR_ROLE_ID = self._DATA['FRANCTIREUR_ROLE_ID']
            self.FUSILIERE_ROLE_ID = self._DATA['FUSILIERE_ROLE_ID']
            self.SAGITTAIRE_ROLE_ID = self._DATA['SAGITTAIRE_ROLE_ID']
            self.ARTILLEUR_ROLE_ID = self._DATA['ARTILLEUR_ROLE_ID']
            self.MACHINISTE_ROLE_ID = self._DATA['MACHINISTE_ROLE_ID']
            self.ARCANISTE_ROLE_ID = self._DATA['ARCANISTE_ROLE_ID']
            self.BARDE_ROLE_ID = self._DATA['BARDE_ROLE_ID']
            self.INVOCATRICE_ROLE_ID = self._DATA['INVOCATRICE_ROLE_ID']
            self.SORCIERE_ROLE_ID = self._DATA['SORCIERE_ROLE_ID']
            self.SANGUELAME_ROLE_ID = self._DATA['SANGUELAME_ROLE_ID']
            self.FAUCHEUSE_ROLE_ID = self._DATA['FAUCHEUSE_ROLE_ID']
            self.DEMONISTE_ROLE_ID = self._DATA['DEMONISTE_ROLE_ID']
            self.ARTISTE_ROLE_ID = self._DATA['ARTISTE_ROLE_ID']
            self.PVP_ROLE_ID = self._DATA['PVP_ROLE_ID']
            self.PVE_ROLE_ID = self._DATA['PVE_ROLE_ID']
            self.MOKOKOS_ROLE_ID = self._DATA['MOKOKOS_ROLE_ID']
            self.RAPPEL_ROLE_ID = self._DATA['RAPPEL_ROLE_ID']
            self.INVITE_ROLE_ID = self._DATA['INVITE_ROLE_ID']

            self.PISTOLANCIER_EMOJI_ID = self._DATA['PISTOLANCIER_EMOJI_ID']
            self.DESTRUCTEUR_EMOJI_ID = self._DATA['DESTRUCTEUR_EMOJI_ID']
            self.BERSERKER_EMOJI_ID = self._DATA['BERSERKER_EMOJI_ID']
            self.PALADIN_EMOJI_ID = self._DATA['PALADIN_EMOJI_ID']
            self.ELEMENTISTE_EMOJI_ID = self._DATA['ELEMENTISTE_EMOJI_ID']
            self.ESSENTIALISTE_EMOJI_ID = self._DATA['ESSENTIALISTE_EMOJI_ID']
            self.SPIRITE_EMOJI_ID = self._DATA['SPIRITE_EMOJI_ID']
            self.PUGILISTE_EMOJI_ID = self._DATA['PUGILISTE_EMOJI_ID']
            self.LANCIERE_EMOJI_ID = self._DATA['LANCIERE_EMOJI_ID']
            self.FRANCTIREUR_EMOJI_ID = self._DATA['FRANCTIREUR_EMOJI_ID']
            self.FUSILIERE_EMOJI_ID = self._DATA['FUSILIERE_EMOJI_ID']
            self.SAGITTAIRE_EMOJI_ID = self._DATA['SAGITTAIRE_EMOJI_ID']
            self.ARTILLEUR_EMOJI_ID = self._DATA['ARTILLEUR_EMOJI_ID']
            self.MACHINISTE_EMOJI_ID = self._DATA['MACHINISTE_EMOJI_ID']
            self.ARCANISTE_EMOJI_ID = self._DATA['ARCANISTE_EMOJI_ID']
            self.BARDE_EMOJI_ID = self._DATA['BARDE_EMOJI_ID']
            self.INVOCATRICE_EMOJI_ID = self._DATA['INVOCATRICE_EMOJI_ID']
            self.SORCIERE_EMOJI_ID = self._DATA['SORCIERE_EMOJI_ID']
            self.SANGUELAME_EMOJI_ID = self._DATA['SANGUELAME_EMOJI_ID']
            self.FAUCHEUSE_EMOJI_ID = self._DATA['FAUCHEUSE_EMOJI_ID']
            self.DEMONISTE_EMOJI_ID = self._DATA['DEMONISTE_EMOJI_ID']
            self.ARTISTE_EMOJI_ID = self._DATA['ARTISTE_EMOJI_ID']
            self.PVP_EMOJI_ID = self._DATA['PVP_EMOJI_ID']
            self.PVE_EMOJI_ID = self._DATA['PVE_EMOJI_ID']
            self.MOKOKOS_EMOJI_ID = self._DATA['MOKOKOS_EMOJI_ID']

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
        super().run(self._TOKEN)

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
        return commands.when_mentioned_or(self.PREFIX)(bot, msg)


    