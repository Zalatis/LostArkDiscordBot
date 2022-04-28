import discord
from datetime import datetime
from discord.ext import commands,tasks

class Image(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.delete_marchands.start()


    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.channel.id != self.bot.MARCHAND_CHANNEL_ID:
            return
        
        if not len(message.attachments):
            return

        try:
            delay = self.get_time(message.content)
        except:
            delay = 7*3600

        try:
            with open ('marchands-messages.txt', 'a+') as f:
                f.seek(0)
                data = f.read()
                if len(data) > 0 :
                    f.write("\n")
                now = datetime.now(self.bot.TIMEZONE)
                ts = datetime.timestamp(now)
                ts_end = ts + delay
                f.write("End at : " + str(ts_end) + " Message ID : " + str(message.id))
                f.close()
        except:
            pass

        # await message.delete(delay=delay)

    def get_time(self,content):
        hms = content.split(':')
        h = int(hms[0])
        m = int(hms[1]) if len(hms)>1 else 0
        s = int(hms[2]) if len(hms)>2 else 0
        return h*3600 + m*60 + s

    @tasks.loop(minutes=1)
    async def delete_marchands(self):
        now = datetime.now(self.bot.TIMEZONE)
        ts = datetime.timestamp(now)
        try:
            with open ('marchands-messages.txt', 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    # print(line)
                    if line.startswith("End at : "):
                        end_at = float(line.split("End at : ")[1].split(" Message ID : ")[0])
                        if ts >= end_at:
                            f.truncate()
                            message_id = int(line.split("Message ID : ")[1])
                            channel = self.bot.get_channel(self.bot.MARCHAND_CHANNEL_ID)
                            message = await channel.fetch_message(message_id)
                            await message.delete()
                        if ts < end_at:
                            f.truncate()
                            f.write(line)
                    elif not line.isspace():
                        f.truncate()
                        f.write(line)
            # last changement
            f.close()
        except:
            pass

def setup(bot:commands.Bot):
    bot.add_cog(Image(bot))