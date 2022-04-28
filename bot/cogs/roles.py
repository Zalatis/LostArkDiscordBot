import discord
from discord.ext import commands

#Cog for discord event handling
class Roles(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        # List of roles for test server
        # format : (name="emoji_name", id=emoji_id): role_id
        self.emoji_to_role = {
            discord.PartialEmoji(name="pistolancier", id=957640668396785684): 957691733032964137,
            # discord.PartialEmoji(name="destructeur", id=0): 0,
            discord.PartialEmoji(name="berserker", id=957640668073824277): 957691749730488331,
            discord.PartialEmoji(name="paladin", id=957640668405182464): 957691763676565635,
            discord.PartialEmoji(name="elementiste", id=957640668497444864): 957691764326695016,
            discord.PartialEmoji(name="essentialiste", id=957640668455526400): 957691765278785576,
            discord.PartialEmoji(name="spirite", id=957640668514250792): 957691765740146718,
            discord.PartialEmoji(name="pugiliste", id=957640668510060574): 957691766776152064,
            discord.PartialEmoji(name="lanciere", id=961633155838771220): 961655213247303772,
            discord.PartialEmoji(name="franctireur", id=957640670242287616): 957691767669551215,
            discord.PartialEmoji(name="fusiliere", id=957640668677820456): 957691767694721115,
            discord.PartialEmoji(name="sagittaire", id=957640668572971028): 957691804424212502,
            discord.PartialEmoji(name="artilleur", id=957697508329529404): 957691931079606342,
            # discord.PartialEmoji(name="machiniste", id=0): 0,
            # discord.PartialEmoji(name="arcaniste", id=0): 0,
            discord.PartialEmoji(name="barde", id=957640668132544584): 957691933025771613,
            # discord.PartialEmoji(name="invocatrice", id=0): 0,
            discord.PartialEmoji(name="sorciere", id=957640668535197737): 957691935227781161,
            # discord.PartialEmoji(name="faucheuse", id=0): 0,
            discord.PartialEmoji(name="sanguelame", id=957640668635856946): 957691937203290123,
            discord.PartialEmoji(name="demoniste", id=957640668363247617): 957691938591621251,
            # discord.PartialEmoji(name="artiste", id=0): 0,
            discord.PartialEmoji(name="pvp", id=957640668463894568): 957691411283730433,
            discord.PartialEmoji(name="pve", id=957640668438749204): 957691715408527450,
            discord.PartialEmoji(name="mokokosanonymes", id=957746859563171940): 957747537576603648,
            discord.PartialEmoji(name="🔔"): 707758009228460123
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.channel_id) != str(self.bot.ROLES_CHANNEL_ID):
            return

        if payload.member.bot == True:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        
        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = self.bot.guild.get_role(role_id)
        if role is None:
            return
        
        try:
            invite_role = self.bot.guild.get_role(int(self.bot.INVITE_ROLE_ID))
            channel = await self.bot.fetch_channel(payload.channel_id)
            # if (payload.emoji.name == "mokokosanonymes" or payload.emoji.id == "957746859563171940") and invite_role in payload.member.roles:
            if (payload.emoji.name == "mokokosanonymes" or payload.emoji.id == "957628781974143026") and invite_role in payload.member.roles:
                await payload.member.remove_roles(invite_role)
            await payload.member.add_roles(role)
            msg = await channel.send(f"{payload.member.mention}, vous avez obtenu le rôle `{role.name}`!")
            await msg.delete(delay=5)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if str(payload.channel_id) != str(self.bot.ROLES_CHANNEL_ID):
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = self.bot.guild.get_role(int(role_id))
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        try:
            invite_role = self.bot.guild.get_role(int(self.bot.INVITE_ROLE_ID))
            channel = await self.bot.fetch_channel(payload.channel_id)
            member = await(await self.bot.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
            # if (payload.emoji.name == "mokokosanonymes" or payload.emoji.id == "957746859563171940") and invite_role not in member.roles:
            if (payload.emoji.name == "mokokosanonymes" or payload.emoji.id == "957628781974143026") and invite_role not in member.roles:
                await member.add_roles(invite_role)
            await member.remove_roles(role)
            msg = await channel.send(f"{member.mention}, vous n'avez plus le rôle `{role.name}`!")
            await msg.delete(delay=5)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(member.guild.id)
        if guild is None:
            return

        invite_role = self.bot.guild.get_role(int(self.bot.INVITE_ROLE_ID))
        if invite_role is None:
            return
        
        if member is None:
            return

        try:
            await member.add_roles(invite_role)
        except discord.HTTPException:
            pass

def setup(bot:commands.Bot):
    bot.add_cog(Roles(bot))
