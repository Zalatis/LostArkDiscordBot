import discord
import re
from discord.ext import commands

class Choices(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.channel.id != int(self.bot.HEBDO_CHOICE_CHANNEL_ID):
            return

        emojis = re.findall(r'<:\w*:\d*>',message.content)
        for x in range(len(emojis)):
            await message.add_reaction(emojis[x])

def setup(bot:commands.Bot):
    bot.add_cog(Choices(bot))