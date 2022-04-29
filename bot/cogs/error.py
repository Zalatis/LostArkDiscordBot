import discord
from discord.ext import commands
import logging

# Custom exceptions
class Error:
    class QueueIsEmpty(commands.CommandError):
        pass
    class QueueIsEnded(commands.CommandError):
        pass

    class NoVoiceChannel(commands.CommandError):
        pass

    class AlreadyConnectedToChannel(commands.CommandError):
        pass
    class TrackAlreadyInQueue(commands.CommandError):
        pass


#Error handler Cog
class ErrorHandler(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    #Error in an application command
    @commands.Cog.listener()
    async def on_command_error(self,ctx: commands.context,exc):

        #If the command has it's own error handler 
        if hasattr(ctx.command,"on_error"):
            return
        
        exc = getattr(exc, "original", exc)
        
        #Unknown command
        if isinstance(exc,commands.CommandNotFound):
            msg = await ctx.send(f"{ctx.author.mention} Votre commande n'existe pas")
            await msg.delete(delay=5)
            await ctx.message.delete(delay=5)
            return

        #Missing Arguments 
        if isinstance(exc,commands.MissingRequiredArgument):
            msg = await ctx.send(f"{ctx.author.mention}, donnez les arguments nécessaires")
            await msg.delete(delay=5)
            await ctx.message.delete(delay=5)
            return 

        #Unexpected error 
        if isinstance(exc,commands.CommandError):
            devs = [discord.Member(id) for id in ctx.bot.DEV_ID]
            await ctx.send(f"Erreur inconnue: {exc}")
            for dev in devs:
                await ctx.send(dev.mention)
            logging.exception(exc)

    #Error in on_message event
    async def on_message_error(self,message,exc):
        exc_org = getattr(exc, "original", exc)
        if not isinstance(exc_org,commands.CommandError):
            logging.exception(exc)
            raise exc
        error_info = ''.join([' '+ s if s.isupper()  else s for s in repr(exc)]).lstrip()
        msg = await message.reply(message.author.mention+" "+error_info[:-2])
        await msg.delete(delay=5)


def setup(bot:commands.Bot):
    bot.add_cog(ErrorHandler(bot))