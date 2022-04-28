import discord
from discord.ext import commands,tasks
from datetime import datetime

class Tasks(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.auto_message.start()

    def cog_unload(self):
        self.auto_message.cancel()

    @tasks.loop(minutes=1)
    async def auto_message(self):
        now = datetime.now(self.bot.TIMEZONE)
        if now.hour==12 and now.minute==0:
            channel = await self.bot.guild.fetch_channel(self.bot.RAPPEL_CHANNEL_ID)
            # embed = discord.Embed(title = "<@&957643253065351210> : N'oubliez pas de faire vos dons de guilde" , color= discord.Color.dark_magenta())
            embed = discord.Embed(title="N'oubliez pas de faire vos dons de guilde", description="<@&" + self.bot.RAPPEL_ROLE_ID + ">", color=discord.Color.dark_magenta())
            await channel.send(embed = embed)

def setup(bot:commands.Bot):
    bot.add_cog(Tasks(bot))