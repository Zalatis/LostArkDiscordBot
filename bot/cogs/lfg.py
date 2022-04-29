import discord
from discord import SlashCommandGroup, slash_command
from discord.commands import Option
from discord.ext import commands

class Lfg(commands.Cog):

    GUILD_IDS = []

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        Lfg.GUILD_IDS.append(int(self.bot.GUILD_ID))

    @slash_command(
        name = "register" , 
        usage="/register" , 
        description = "Enregistre un personnage dans ton profil" ,
        guild_ids=GUILD_IDS
    )
    async def register(self,
    ctx, 
    nom_du_personnage : Option(str, "Saisissez le nom de votre personnage", required = True),
    ilvl : Option(str, "Saisissez l'ilvl de votre personnage", required = True),
    classe : Option(str, "Choisissez la classe de votre personnage", required = True, choices=["Arcaniste","Artilleur","Artiste", "Barde", "Berserker", "Démoniste", "Destructeur", "Élémentiste", "Essentialiste", "Faucheuse", "Fusilière", "Franc-Tirreur", "Invocatrice", "Lancière", "Machiniste", "Paladin", "Pistolancier", "Pugiliste", "Sagittaire", "Sanguelame", "Sorcière", "Spirite"])):
        
        if nom_du_personnage is None:
            await ctx.respond("Veuillez entrer un nom de personnage", ephemeral=True)
            return

        if ilvl is None:
            await ctx.respond("Veuillez entrer un ilvl", ephemeral=True)
            return
    
        if classe is None:
            await ctx.respond("Veuillez entrer une classe", ephemeral=True)
            return

        await ctx.respond(f"Nom du personnage : `{nom_du_personnage}`, Ilvl : `{ilvl}`, Classe : `{classe}`", ephemeral=True)

def setup(bot:commands.Bot):
    bot.add_cog(Lfg(bot))