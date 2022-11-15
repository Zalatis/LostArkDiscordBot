import discord
from discord.ext import commands
from discord.commands import slash_command,Option, SlashCommandGroup
from discord.utils import basic_autocomplete
from discord import ui

# TODO Needs edit format [content_name , max difficulty]
lobby_contents = [
    ["Content 1", 3],
    ["Content 2", 5],
    ["Content 3", 1],
    ["Content 4", 2],
    ["Content 5", 3],
    ["Content 6", 4],
    ["Content 7", 3],
]



class Lfg(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.db = self.bot.db

    def get_embed(self,title : str, description : str ,party_leader : discord.Member):
        embed = discord.Embed(title= title , description= description , color= discord.Color.random())
        embed.set_author(name= "Party Leader "+party_leader.display_name, icon_url= party_leader.display_avatar.url)
        return embed

    @slash_command(description = "Put description for LFG")
    async def lfg(self, ctx:commands.Context, *, custom_message:str):

        embed = self.get_embed(
            title = "Welcome to Lost Ark Bot LFG!", 
            description= "Choose from the list below which content you would like to open a recruitment lobby for.",
            party_leader = ctx.author
        )

        view = ui.View()
        view.add_item(self.Select(placeholder= "Select Content" , items= [content[0] for content in lobby_contents] ))

        await ctx.respond(custom_message,embed = embed , view = view)

    class Select(ui.Select):
        def __init__(self, placeholder : str, items : list ):
            self.items = items
            options = [ discord.SelectOption(label = option) for option in items ]

            super().__init__(placeholder = placeholder, options = options)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.edit_message(content= "You selected: " + self.values[0])


def setup(bot:commands.Bot):
    bot.add_cog(Lfg(bot))

