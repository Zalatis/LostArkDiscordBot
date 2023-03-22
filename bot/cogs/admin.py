import discord
from discord import SlashCommandGroup, slash_command
from discord.commands import permissions
from discord.ext import commands
import json





# Admin/Dev only commands
class Admin(commands.Cog):

    GUILD_IDS = []
    PERMITED_ROLES_IDS = []

    def __init__(self, bot:commands.Bot):

        self.bot = bot

        Admin.GUILD_IDS.append(int(self.bot.GUILD_ID))
        Admin.PERMITED_ROLES_IDS.append(self.bot.PERMITED_ROLES_IDS)


    async def cog_check(self, ctx: discord.ApplicationContext):
        if not ctx.guild:
            interaction = await ctx.respond(f"{ctx.command.name} est une commande lié au serveur.")
            await interaction.delete_original_message(delay=5)
            return False

        if not any(permited_role in str(ctx.author.roles) for permited_role in ctx.bot.PERMITED_ROLES_IDS):
            interaction = await ctx.respond(f"{ctx.command.name} est une commande réservée aux administrateurs.")
            await interaction.delete_original_message(delay=5)
            return False

        return True

    @slash_command(
        name = "roles" , 
        usage="/roles" , 
        description = "Créer le message de rôles dans le canal de texte (Admin seulement)" ,
        guild_ids=GUILD_IDS
    )
    @commands.has_any_role(*PERMITED_ROLES_IDS)
    async def role(self,ctx):
        if not await self.cog_check(ctx):
            return 
        
        interaction = await ctx.respond("Envoi du message pour les roles")

        # Roles Guerriers
        embed = discord.Embed(title="Guerriers", description="Vous trouverez ci-dessous les rôles liés à la classe **Guerrier**" , color= discord.Color.from_rgb(208,179,115))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958088471703072808/ArchetypeWarrior.png")
        embed.add_field(name="Pistolancier:", value= "<"+ self.bot.PISTOLANCIER_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Destructeur:", value= "<"+ self.bot.DESTRUCTEUR_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Berserker:", value= "<"+ self.bot.BERSERKER_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Paladin:", value= "<"+ self.bot.PALADIN_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.PISTOLANCIER_EMOJI_ID)
        await msg.add_reaction(self.bot.DESTRUCTEUR_EMOJI_ID)
        await msg.add_reaction(self.bot.BERSERKER_EMOJI_ID)
        await msg.add_reaction(self.bot.PALADIN_EMOJI_ID)

        # Roles Martialiste
        embed = discord.Embed(title="Martialistes", description="Vous trouverez ci-dessous les rôles liés à la classe **Martialiste**" , color= discord.Color.from_rgb(117,169,213))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958088470860021830/ArchetypeFighter.png")
        embed.add_field(name="Elementiste:", value= "<"+ self.bot.ELEMENTISTE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Essentialiste:", value= "<"+ self.bot.ESSENTIALISTE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Spirite:", value= "<"+ self.bot.SPIRITE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Pugiliste:", value= "<"+ self.bot.PUGILISTE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Lancière:", value= "<"+ self.bot.LANCIERE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="​", value= "​​", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.ELEMENTISTE_EMOJI_ID)
        await msg.add_reaction(self.bot.ESSENTIALISTE_EMOJI_ID)
        await msg.add_reaction(self.bot.SPIRITE_EMOJI_ID)
        await msg.add_reaction(self.bot.PUGILISTE_EMOJI_ID)
        await msg.add_reaction(self.bot.LANCIERE_EMOJI_ID)

        # Roles Tireur d'élite
        embed = discord.Embed(title="Tireurs d'élite", description="Vous trouverez ci-dessous les rôles liés à la classe **Tireur d'élite**" , color= discord.Color.from_rgb(184,97,132))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958088471107502120/ArchetypeHunter.png")
        embed.add_field(name="Franc-tireur:", value= "<"+ self.bot.FRANCTIREUR_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Fusilière:", value= "<"+ self.bot.FUSILIERE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Sagittaire:", value= "<"+ self.bot.SAGITTAIRE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Artilleur:", value= "<"+ self.bot.ARTILLEUR_EMOJI_ID + ">", inline=True)
        # embed.add_field(name="Machiniste:", value= "<"+ self.bot.MACHINISTE_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.FRANCTIREUR_EMOJI_ID)
        await msg.add_reaction(self.bot.FUSILIERE_EMOJI_ID)
        await msg.add_reaction(self.bot.SAGITTAIRE_EMOJI_ID)
        await msg.add_reaction(self.bot.ARTILLEUR_EMOJI_ID)
        # await msg.add_reaction(self.bot.MACHINISTE_EMOJI_ID)

        # Roles Mage
        embed = discord.Embed(title="Mages", description="Vous trouverez ci-dessous les rôles liés à la classe **Mage**"  , color= discord.Color.from_rgb(164,111,214))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958088471329796186/ArchetypeMagician.png")
        # embed.add_field(name="Arcaniste", value= "<"+ self.bot.ARCANISTE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Barde:", value= "<"+ self.bot.BARDE_EMOJI_ID + ">", inline=True)
        # embed.add_field(name="Invocatrice", value= "<"+ self.bot.INVOCATRICE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Sorcière:", value= "<"+ self.bot.SORCIERE_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        # await msg.add_reaction(self.bot.ARCANISTE_EMOJI_ID)
        await msg.add_reaction(self.bot.BARDE_EMOJI_ID)
        # await msg.add_reaction(self.bot.INVOCATRICE_EMOJI_ID)
        await msg.add_reaction(self.bot.SORCIERE_EMOJI_ID)

        # Roles Assassin
        embed = discord.Embed(title="Assassins", description="Vous trouverez ci-dessous les rôles liés à la classe **Assassin**"  , color= discord.Color.from_rgb(96,205,181))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958089128623366164/ArchetypeAssassin.png")
        embed.add_field(name="Sanguelame:", value= "<"+ self.bot.SANGUELAME_EMOJI_ID + ">", inline=True)
        # embed.add_field(name="Faucheuse", value= "<"+ self.bot.FAUCHEUSE_EMOJI_ID + ">", inline=True)
        embed.add_field(name="Démoniste:", value= "<"+ self.bot.DEMONISTE_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.SANGUELAME_EMOJI_ID)
        # await msg.add_reaction(self.bot.FAUCHEUSE_EMOJI_ID)
        await msg.add_reaction(self.bot.DEMONISTE_EMOJI_ID)

        # Roles Spécialiste
        embed = discord.Embed(title="Spécialistes", description="Vous trouverez ci-dessous les rôles liés à la classe **Spécialiste**"  , color= discord.Color.from_rgb(134,161,133))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958088471514325012/ArchetypeSpecialist.png")
        embed.add_field(name="Artiste:", value= "<"+ self.bot.ARTISTE_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.ARTISTE_EMOJI_ID)

        # Roles PvP/PvE
        embed = discord.Embed(title="Modes de jeu", description="Vous trouverez ci-dessous les rôles liés aux **modes de jeu**"  , color= discord.Color.from_rgb(174,171,212))
        embed.add_field(name="PvP:", value= "<"+ self.bot.PVP_EMOJI_ID + ">", inline=True)
        embed.add_field(name="PvE:", value= "<"+ self.bot.PVE_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.PVP_EMOJI_ID)
        await msg.add_reaction(self.bot.PVE_EMOJI_ID)

        # Roles Mokokos Anonymes
        embed = discord.Embed(title="Les Mokokos Anonymes", description="Clique sur le mokoko ci-dessous si tu fais partie de la guilde **Les Mokokos Anonymes**"  , color= discord.Color.from_rgb(197,237,140))
        # embed.add_field(name="Les Mokokos Anonymes:", value= "<"+ self.bot.MOKOKOS_EMOJI_ID + ">", inline=True)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction(self.bot.MOKOKOS_EMOJI_ID)

        # Role Rappel
        embed = discord.Embed(title="Rappel", description="Clique sur la cloche ci-dessous pour avoir les notifications des rappels de dons quotidiens"  , color= discord.Color.from_rgb(237,196,87))
        msg = await ctx.channel.send(embed = embed)
        # await msg.pin()
        await msg.add_reaction("🔔")
        
        await interaction.delete_original_message()

    @slash_command(
        name = "welcome" , 
        usage="/welcome" , 
        description = "Créer le message de bienvenue (Admin seulement)" ,
        guild_ids=GUILD_IDS
    )
    @commands.has_any_role(*PERMITED_ROLES_IDS)
    async def welcome(self,ctx):
        if not await self.cog_check(ctx):
            return 

        interaction = await ctx.respond("Envoi du message de bienvenue")
        embed=discord.Embed(title="Salut Voyageur !", description="Bienvenue sur le discord de la guilde Lost Ark des Mokokos Anonymes, que vous soyez membre de la guilde, de l'alliance, fan de mokokos ou un invité, vous êtes le bienvenu.", color=discord.Color.blue())
        embed.set_author(name="MaajiN", icon_url="https://cdn.discordapp.com/avatars/174605384680472576/64b6e8f2165f5966630f851615133f41.webp?size=32")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/277197386772774912/957622310305689621/logo_discord.png")
        embed.add_field(name="__Présentation :__", value="La guilde évolue principalement sur le serveur Trixion avec des membres présents sur d'autres serveurs tels que Neria, ici pas de prérequis pour intégrer la guilde, seule une bonne humeur et de l'entente entre membres est de mise.", inline=False)
        embed.add_field(name="__Informations : __", value="Lors de chaque reset hebdomadaire le jeudi, les membres de la guilde peuvent voter pour les quêtes de guildes dans : <#" + self.bot.HEBDO_CHOICE_CHANNEL_ID + ">, les news concernant le jeu et ses mises à jour sont automatiquement postées dans le channel <#" + self.bot.NEWS_CHANNEL_ID + "> via <@" + self.bot.BOT_ID + "> développé par <@" + self.bot.DEV_ID + ">.", inline=False)
        embed.add_field(name="__Rôles et alertes :__", value="Dans <#" + self.bot.ROLES_CHANNEL_ID + ">, vous pouvez réagir avec les émojis liées aux classes que vous jouez, et si vous faites partie de la guilde `Les Mokokos Anonymes`. Vous pouvez également utliser l'émoji 🔔 pour activer les alertes vous rappelant chaque jour de contribuer à la guilde via votre don quotidien et le soutien de la ou les recherches en cours !", inline=False)
        embed.add_field(name="__Ressources :__", value="Pour les débutants ou les joueurs cherchant de l'aide, le salon <#" + self.bot.RESSOURCES_CHANNEL_ID + "> est à disposition, vous y trouverez notamment les différentes cartes interactives, les builds, les guides et autres ressources importantes pour vous épauler.", inline=False)
        await ctx.send(embed = embed)
        
        await interaction.delete_original_message()

    @slash_command(
        name = "move" , 
        usage="/move" , 
        description = "Déplacer toutes les personnes d'un salon dans un autre" ,
        guild_ids=GUILD_IDS,
        default_permissions = False 
    )
    @commands.has_any_role(*PERMITED_ROLES_IDS)
    async def move(self,ctx, de: discord.VoiceChannel, vers: discord.VoiceChannel):
        if not await self.cog_check(ctx):
            return 

        if de == vers:
            interaction = await ctx.respond("Impossible de déplacer dans le même salon.")
            await interaction.delete_original_message(delay=5)
            return

        tot =  len(de.members)
        
        if not tot:
            interaction = await ctx.respond("Il n'y a personne dans ce salon")
            await interaction.delete_original_message(delay=5)
            return

        for member in de.members:
            await member.move_to(vers)

        # msg = await ctx.respond(f"`{tot}` p. `{de.name}` > `{vers.name}`")
        interaction = await ctx.respond(f"`{tot}` p. `{de.name}` > `{vers.name}`", ephemeral=True)

    # @slash_command(
    #     name = "update_roles" , 
    #     usage="/update_roles" , 
    #     description = "Met à jour le système de rôles par réaction (Admin seulement)" ,
    #     guild_ids=GUILD_IDS
    # )
    # @permissions.has_any_role(*PERMITED_ROLES_IDS)
    # async def update_roles(self,ctx):
    #     if not await self.cog_check(ctx):
    #         return 
        
    #     interaction = await ctx.respond("Mise à jour en cours...")

    #     # Roles Guerries
    #     channel = await self.bot.guild.fetch_channel(int(self.bot.ROLES_CHANNEL_ID))
    #     msg = await channel.fetch_message("959174550640295956")
    #     embed = discord.Embed(title="Guerriers", description="Vous trouverez ci-dessous les rôles liés à la classe **Guerrier**" , color= discord.Color.from_rgb(208,179,115))
    #     embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/277197386772774912/958088471703072808/ArchetypeWarrior.png")
    #     embed.add_field(name="Pistolancier:", value= "<"+ self.bot.PISTOLANCIER_EMOJI_ID + ">", inline=True)
    #     embed.add_field(name="Destructeur:", value= "<"+ self.bot.DESTRUCTEUR_EMOJI_ID + ">", inline=True)
    #     embed.add_field(name="Berserker:", value= "<"+ self.bot.BERSERKER_EMOJI_ID + ">", inline=True)
    #     embed.add_field(name="Paladin:", value= "<"+ self.bot.PALADIN_EMOJI_ID + ">", inline=True)
    #     await msg.add_reaction(self.bot.PISTOLANCIER_EMOJI_ID)
    #     await msg.add_reaction(self.bot.DESTRUCTEUR_EMOJI_ID)
    #     await msg.add_reaction(self.bot.BERSERKER_EMOJI_ID)
    #     await msg.add_reaction(self.bot.PALADIN_EMOJI_ID)
    #     await msg.edit(embed = embed)
        
    #     await interaction.delete_original_message()
    
    # @slash_command(
    #     name = "update_welcome" , 
    #     usage="/update_welcome" , 
    #     description = "Met à jour le message de bienvenue (Admin seulement)" ,
    #     guild_ids=GUILD_IDS
    # )
    # @permissions.has_any_role("Leader Stratège" , "Leader Mokokos Anonymes", "Officier Mokokos Anonymes")
    # async def update_welcome(self,ctx):
    #     if not await self.cog_check(ctx):
    #         return 
        
    #     interaction = await ctx.respond("Mise à jour en cours...")

    #     channel = await self.bot.guild.fetch_channel(int("947866179593187338"))
    #     msg = await channel.fetch_message("959174510484000818")
    #     embed=discord.Embed(title="Salut Voyageur !", description="Bienvenue sur le discord de la guilde Lost Ark des Mokokos Anonymes, que vous soyez membre de la guilde, de l'alliance, fan de mokokos ou un invité, vous êtes le bienvenu.", color=discord.Color.blue())
    #     embed.set_author(name="MaajiN", icon_url="https://cdn.discordapp.com/avatars/174605384680472576/64b6e8f2165f5966630f851615133f41.webp?size=32")
    #     embed.set_thumbnail(url="https://media.discordapp.net/attachments/277197386772774912/957622310305689621/logo_discord.png")
    #     embed.add_field(name="__Présentation :__", value="La guilde évolue principalement sur le serveur Trixion avec des membres présents sur d'autres serveurs tels que Neria, ici pas de prérequis pour intégrer la guilde, seule une bonne humeur et de l'entente entre membres est de mise.", inline=False)
    #     embed.add_field(name="__Informations : __", value="Lors de chaque reset hebdomadaire le jeudi, les membres de la guilde peuvent voter pour les quêtes de guildes dans : <#" + self.bot.HEBDO_CHOICE_CHANNEL_ID + ">, les news concernant le jeu et ses mises à jour sont automatiquement postées dans le channel <#" + self.bot.NEWS_CHANNEL_ID + "> via <@" + self.bot.BOT_ID + "> développé par <@" + self.bot.DEVS + ">.", inline=False)
    #     embed.add_field(name="__Rôles et alertes :__", value="Dans <#" + self.bot.ROLES_CHANNEL_ID + ">, vous pouvez réagir avec les émojis liées aux classes que vous jouez, et si vous faites partie de la guilde `Les Mokokos Anonymes`. Vous pouvez également utliser l'émoji 🔔 pour activer les alertes vous rappelant chaque jour de contribuer à la guilde via votre don quotidien et le soutien de la ou les recherches en cours !", inline=False)
    #     embed.add_field(name="__Ressources :__", value="Pour les débutants ou les joueurs cherchant de l'aide, le salon <#" + self.bot.RESSOURCES_CHANNEL_ID + "> est à disposition, vous y trouverez notamment les différentes cartes interactives, les builds, les guides et autres ressources importantes pour vous épauler.", inline=False)
    #     await msg.edit(embed = embed)
        
    #     await interaction.delete_original_message()

def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))

