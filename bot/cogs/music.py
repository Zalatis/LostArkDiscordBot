import discord
from random import choices
from discord.ext import commands
from discord import SlashCommandGroup, slash_command, Interaction, ui
from discord.commands import Option, permissions
import wavelink
import logging

from .music_files import player,track,api
from .music_files.player import Player
from .music_files.track import Track
from bot.cogs.error import Error

class Music(commands.Cog):

    GUILD_IDS = []
    PERMITED_ROLES_IDS = []

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        Music.GUILD_IDS.append(int(self.bot.GUILD_ID))
        Music.PERMITED_ROLES_IDS.append(self.bot.PERMITED_ROLES_IDS)
        # print(Music.PERMITED_ROLES_IDS)

        bot.loop.create_task(self.connect_nodes())

    # Default checks for all commands in the cog
    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send('Les commandes de musique ne sont pas disponibles en messages privés')
            return False

        if not any(permited_role in str(ctx.author.roles) for permited_role in ctx.bot.PERMITED_ROLES_IDS):
            interaction = await ctx.respond(f"{ctx.command.name} est une commande réservée aux administrateurs.")
            await interaction.delete_original_message(delay=5)
            return False

        return True

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node):
        print(f"Wavelink node '{node.identifier}' ready.")

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        self.bot.node = await wavelink.NodePool.create_node(bot=self.bot,
                                                            host='127.0.0.1',  # '172.31.21.15',
                                                            port=2333,
                                                            password='youshallnotpass')

    async def get_player(self, payload: discord.RawReactionActionEvent):
        if not payload.member.voice or (channel:=payload.member.voice.channel) is None:
            raise Error.NoVoiceChannel
        if pl:=self.bot.node.get_player(self.bot.get_guild(payload.guild_id)):
            if pl.is_connected():
                if pl.channel==channel:
                    return pl
                raise Error.AlreadyConnectedToChannel
        return await channel.connect(cls=Player)


    # listeners
    @commands.Cog.listener()
    async def on_wavelink_track_end(self,player: Player, track: Track, reason):
        if(reason=="REPLACED" or reason=="STOPPED"):
            return
        logging.info(reason)
        await player.next_track()

    @commands.Cog.listener()
    async def on_wavelink_track_exception(self,player: Player, track: Track,error):
        logging.warning(error)

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self,player: Player, track: Track,threshold):
        logging.warning('threshold: '+threshold)
        player.restart_track()

    @commands.Cog.listener()
    async def on_wavelink_websocket_closed(self,player,reason,code):
        await player.cleanup_and_disconnect()

    async def get_player(self, author: discord.Member, guild: discord.Guild):
        if not author.voice or (channel:=author.voice.channel) is None:
            raise Error.NoVoiceChannel
        if pl:=self.bot.node.get_player(guild):
            if pl.is_connected():
                if pl.channel==channel:
                    return pl
                raise Error.AlreadyConnectedToChannel
        return await channel.connect(cls=player.Player)

    # Commands
    @slash_command(
        name = "play" , 
        usage="/play" , 
        description = "Joue la musique choisie via recherche, lien youtube ou lien spotify" ,
        guild_ids=GUILD_IDS
    )
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def play(
        self,
        ctx:commands.Context,
        méthode: Option(str,"Sélectionnez recherche/lien",choices=["Recherche","Lien Youtube","Lien Spotify"]),
        requête: Option(str, "Collez le lien ou tapez quoi rechercher (en fonction de la méthode choisie)")
    ):
        try:
            vc = await self.get_player(ctx.author,ctx.guild)
        except Error.NoVoiceChannel:
            interaction = await ctx.respond(f"{ctx.author.mention}, tu dois d'abord être dans un canal vocal")
            return await interaction.delete_original_message(delay=5)
        except Error.AlreadyConnectedToChannel:
            interaction = await ctx.respond(f"{ctx.author.mention}, musique déjà en lecture dans {ctx.guild.voice_client.channel}")
            return await interaction.delete_original_message(delay=5)


        if méthode == "Recherche":
            youtubeTrack = await api.searchYoutube(self.bot,requête)
            if not track:
                return await ctx.respond("Pas de chanson trouvée")

        elif méthode == "Lien Youtube":
            link = api.checkYoutube(requête)
            if not link:
                return await ctx.respond("Lien Youtube invalide")

            try:
                youtubeTrack = await api.getYoutubeTrack(self.bot,link)
            except:
                return await ctx.respond("Lien invalide ou Youtube ne répond pas")

        elif méthode == "Lien Spotify":
            link = api.checkSpotify(requête)
            if not link:
                return await ctx.respond("Lien Spotify invalide")

            try:
                spotifyTrack = await api.getSpotifyTrack(self.bot,link)
            except:
                return await ctx.respond("Lien invalide ou Spotify ne répond pas")

            requête = spotifyTrack["name"] + " " + spotifyTrack["artists"][0]["name"]
            youtubeTrack = await api.searchYoutube(self.bot,requête)

        else:
            return await ctx.respond("Méthode invalide")

        song = track.Track(self.bot,ctx.author,youtubeTrack)
        response = f" `{song.get_title()}` ajouté à la file d'attente"
        try:
            await vc.add_track(song,ctx.channel)
        except Error.TrackAlreadyInQueue:
            response = f" `{song.get_title()}` est déjà dans la file d'attente"
        
        interaction = await ctx.respond(ctx.author.name+response)
        await interaction.delete_original_message(delay=5)

    @slash_command(
        name = "dc" , 
        usage="/dc" , 
        description = "Déconnecte le bot du salon vocal" ,
        guild_ids=GUILD_IDS,
        default_permissions = False 
    )
    @commands.has_any_role(*PERMITED_ROLES_IDS)
    async def dc(self,ctx):
        if not await self.cog_check(ctx):
            return 

        if pl:=self.bot.node.get_player(ctx.author.guild):
            if pl.is_connected():
                channel_name = ctx.guild.voice_client.channel.name
                await pl.cleanup_and_disconnect()
                await ctx.respond(f"Le bot s'est déconnecté du salon vocal `{channel_name}`", ephemeral=True)
        else:
            await ctx.respond(f"{ctx.author.mention} Le bot n'est pas connecté à un salon vocal", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))


