import discord
from discord.ext import commands
from discord.commands import slash_command,Option, SlashCommandGroup
from discord.utils import basic_autocomplete
from discord import ui

char_classes = [
    "Pistolancier",
    "Destructeur",
    "Berserker",
    "Paladin",
    "Elementiste",
    "Essentialiste",
    "Spirite",
    "Pugiliste",
    "Lancière",
    "Franc-Tirreur",
    "Fusilière",
    "Sagittaire",
    "Artilleur",
    "Machiniste",
    "Arcaniste",
    "Barde",
    "Invocatrice",
    "Sorcière",
    "Sanguelame",
    "Faucheuse",
    "Démoniste",
    "Artiste"
]

DB = None

def all_characters(ctx:discord.AutocompleteContext):
    # chars = [ item["char_name"].lower() for item in DB.find_all(ctx.interaction.user.id) ]
    user_id = ctx.interaction.user.id
    chars = {
        item["char_name"] 
        for item in DB.characters.find_all(user_id) 
    }
    print(chars)
    return list(chars)

class Lfg(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.db = self.bot.db
        global DB
        DB = self.db

    def get_embed(self, item , page = 0 , total_page = 0):
        embed = discord.Embed(title= item["char_name"] , color= discord.Color.random())
        user = self.bot.get_user(int(item["user_id"]))

        embed.add_field(name="Created by", value= user.name)
        embed.add_field(name="Level", value= item["char_level"])
        embed.add_field(name="Class", value= item["char_class"])

        if total_page:
            embed.set_footer(text= f"Page {page}/{total_page}")

        return embed

    slashgroup = SlashCommandGroup("lobby", description="Commands for lobby and registering/modifying characters")

    @slashgroup.command(description = "Register a new character")
    async def register(
        self, 
        ctx:discord.ApplicationContext,
        char_name:  Option( str, description = "Enter your character's name"), 
        char_level: Option( int, description = "Enter your character's level" , min_value = 1 ), 
        char_class: Option( str, description = "Enter your character's class", choices = char_classes)
    ):
        user_id = ctx.author.id
        char_level = int(char_level)

        item = self.db.characters.get(user_id, char_name, char_level, char_class)

        if item is not None:
            return await ctx.respond("This character is already registered", embed= self.get_embed(item))
        
        item = self.db.characters.register(user_id, char_name, char_level, char_class)

        await ctx.respond("Registered character.", embed= self.get_embed(item))

    @slashgroup.command(description = "Edit an existing character")
    async def edit(
        self,
        ctx:discord.ApplicationContext, 
        char_name: Option( str, description = "Enter your character's name", autocomplete = basic_autocomplete(all_characters)), 
        char_level: Option( int, description = "Enter your character's new level" , min_value = 1 ), 
    ):
        user_id = ctx.author.id
        
        if len(list(self.db.characters.find(user_id,char_name))) == 0:
            return await ctx.respond("No character named "+ char_name + " found", ephemeral = True)

        char_level = int(char_level)
        classes = { 
            item["char_class"] 
            for item in self.db.characters.find(user_id,char_name)
            if item["char_level"] == char_level 
        }

        chars = [
            item 
            for item in self.db.characters.find(user_id,char_name) 
            if item["char_class"] not in classes
        ]

        if not len(chars):
            return await ctx.respond(
                f"There is a character with level `{char_level}` in every class that `{char_name}` is in",
                ephemeral = True
            )

        view = self.get_view(chars,self.get_embed, "edit", level = char_level)

        await ctx.respond(
            "Select which character you want to edit", 
            embed = self.get_embed(chars[0],1,len(chars)), 
            view = view,
            ephemeral = True
        )

    @slashgroup.command(description = "Delete a Character")
    async def delete(
        self,
        ctx:discord.ApplicationContext, 
        char_name: Option( str, description = "Enter your character's name", autocomplete = basic_autocomplete(all_characters)), 
    ):
        user_id = ctx.author.id
        chars = list(self.db.characters.find(user_id,char_name))

        if not len(chars):
            return await ctx.respond("No character named "+ char_name + " found", ephemeral = True)

        view = self.get_view(chars,self.get_embed, "delete")

        await ctx.respond(
            "Select which character you want to delete",
            embed = self.get_embed(chars[0],1,len(chars)),
            view = view,
            ephemeral = True
        )

    class view(ui.View):
        def __init__(self,chars,get_embed , type = "default", level=0):
            self.chars = chars
            self._page = 1
            self.level = level
            self._total_page = len(chars)
            self.get_embed = get_embed

            super().__init__(timeout=30)




        async def update(self,interaction):
            embed = self.get_embed(self.chars[self._page -1], self._page, self._total_page)
            await interaction.response.edit_message(embed = embed,view=self)

        @ui.button(emoji="◀️")
        async def previous_page(self,button,interaction):
            if self._page == 1:
                self._page = self._total_page
            else:
                self._page = self._page - 1 
            await self.update(interaction)

        @ui.button(emoji="▶️")
        async def next_page(self,button,interaction):
            if self._page == self._total_page:
                self._page = 1
            else:
                self._page = self._page + 1 
            await self.update(interaction)
       

        class Button(ui.Button):
            def __init__(self, callback , label = None, emoji = None):
                self.custom_callback = callback
                super().__init__( label = label, emoji = emoji)

            async def callback(self,interaction):
                await self.custom_callback(self,interaction)

    def get_view(self,chars,get_embed , type = "default", level=0):
        view = self.view(chars,get_embed , type = type, level = level)

        async def edit(button,interaction):
            item = button.view.chars[button.view._page -1]
            DB.characters.edit(item["_id"],button.view.level)
            item["char_level"] = button.view.level
            await interaction.response.edit_message(
                content = "Edited character",
                embed = self.get_embed(item),
                view = None                                               
            ) 
        if type == "edit":
            view.add_item(view.Button(callback = edit, label = "Edit", emoji = "⚙️")) 

        async def delete(button,interaction):
            item = button.view.chars[button.view._page -1]
            DB.characters.delete(item["_id"])
            await interaction.response.edit_message(
                content = "Deleted character",
                embed = None,
                view = None                                               
            )
        if type == "delete":
            view.add_item(view.Button(callback = delete, label = "Delete", emoji = "🚫")) 

        return view

def setup(bot:commands.Bot):
    bot.add_cog(Lfg(bot))

