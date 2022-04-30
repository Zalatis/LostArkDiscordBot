import discord
from discord.ext import commands

#Cog for discord event handling
class Roles(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        # List of roles
        # format : (name="emoji_name", id=emoji_id): role_id
        self.emoji_to_role = {
            discord.PartialEmoji(name="".join(self.bot.PISTOLANCIER_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.PISTOLANCIER_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.PISTOLANCIER_ROLE_ID),
            # discord.PartialEmoji(name="".join(self.bot.DESTRUCTEUR_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.DESTRUCTEUR_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.DESTRUCTEUR_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.BERSERKER_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.BERSERKER_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.BERSERKER_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.PALADIN_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.PALADIN_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.PALADIN_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.ELEMENTISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.ELEMENTISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.ELEMENTISTE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.ESSENTIALISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.ESSENTIALISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.ESSENTIALISTE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.SPIRITE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.SPIRITE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.SPIRITE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.PUGILISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.PUGILISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.PUGILISTE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.LANCIERE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.LANCIERE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.LANCIERE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.FRANCTIREUR_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.FRANCTIREUR_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.FRANCTIREUR_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.FUSILIERE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.FUSILIERE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.FUSILIERE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.SAGITTAIRE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.SAGITTAIRE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.SAGITTAIRE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.ARTILLEUR_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.ARTILLEUR_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.ARTILLEUR_ROLE_ID),
            # discord.PartialEmoji(name="".join(self.bot.MACHINISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.MACHINISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.MACHINISTE_ROLE_ID),
            # discord.PartialEmoji(name="".join(self.bot.ARCANISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.ARCANISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.ARCANISTE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.BARDE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.BARDE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.BARDE_ROLE_ID),
            # discord.PartialEmoji(name="".join(self.bot.INVOCATRICE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.INVOCATRICE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.INVOCATRICE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.SORCIERE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.SORCIERE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.SORCIERE_ROLE_ID),
            # discord.PartialEmoji(name="".join(self.bot.FAUCHEUSE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.FAUCHEUSE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.FAUCHEUSE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.SANGUELAME_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.SANGUELAME_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.SANGUELAME_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.DEMONISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.DEMONISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.DEMONISTE_ROLE_ID),
            # discord.PartialEmoji(name="".join(self.bot.ARTISTE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.ARTISTE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.ARTISTE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.PVP_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.PVP_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.PVP_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.PVE_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.PVE_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.PVE_ROLE_ID),
            discord.PartialEmoji(name="".join(self.bot.MOKOKOS_EMOJI_ID.split(":", 2)[:2]), id=int("".join(self.bot.MOKOKOS_EMOJI_ID.split(":", -1)[-1:]))): int(self.bot.MOKOKOS_ROLE_ID),
            discord.PartialEmoji(name="🔔"): int(self.bot.RAPPEL_ROLE_ID)
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != self.bot.ROLES_CHANNEL_ID:
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
            if (payload.emoji.name == "".join(self.bot.MOKOKOS_EMOJI_ID.split(":", 2)[:2]) or payload.emoji.id == int("".join(self.bot.MOKOKOS_EMOJI_ID.split(":", -1)[-1:]))) and invite_role in payload.member.roles:
                await payload.member.remove_roles(invite_role)
            await payload.member.add_roles(role)
            msg = await channel.send(f"{payload.member.mention}, vous avez obtenu le rôle `{role.name}`!")
            await msg.delete(delay=5)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != self.bot.ROLES_CHANNEL_ID:
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
            if (payload.emoji.name == "".join(self.bot.MOKOKOS_EMOJI_ID.split(":", 2)[:2]) or payload.emoji.id == int("".join(self.bot.MOKOKOS_EMOJI_ID.split(":", -1)[-1:]))) and invite_role not in member.roles:
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
