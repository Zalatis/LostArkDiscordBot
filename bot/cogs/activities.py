import discord
from discord import SlashCommandGroup, slash_command
from discord.ext import commands

# Activities
class Activities(commands.Cog):

    GUILD_IDS = []

    def __init__(self, bot:commands.Bot):

        self.bot = bot
        Activities.GUILD_IDS.append(int(self.bot.GUILD_ID))

    @slash_command(
        name = "youtube" , 
        usage="/youtube" , 
        description = "Lance l'activité Youtube Together" ,
        guild_ids=GUILD_IDS
    )
    async def youtube(self, ctx, channel: discord.VoiceChannel = None):
        try:
            if channel == None and ctx.author.voice.channel != None:
                channel = ctx.author.voice.channel
                link = await channel.create_activity_invite(discord.enums.EmbeddedActivity.watch_together, unique = False)
                await ctx.respond(f"[Clique ici pour rejoindre l'activité Youtube Together](<{link}>) !")
            elif channel != None:
                link = await channel.create_activity_invite(discord.enums.EmbeddedActivity.watch_together, unique = False)
                await ctx.respond(f"[Clique ici pour rejoindre l'activité Youtube Together](<{link}>) !")
            else:
                ctx.respond("Vous devez être dans un salon ou définir un salon vocal pour utiliser cette commande.")
        except:
            await ctx.respond("Vous devez être dans un salon ou définir un salon vocal pour utiliser cette commande.")

def setup(bot:commands.Bot):
    bot.add_cog(Activities(bot))