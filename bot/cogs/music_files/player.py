import discord
from discord import has_any_role, ui
import wavelink
import logging

from .track import Track
from bot.cogs.error import Error

class Player(wavelink.Player):

    class Loop:
        OFF = 0
        ONE = 1
        ALL = 2

        name = ["Désactivé","En lecture actuellement","Liste de lecture"]

    class Emoji:
        play = "▶️"     
        pause = "⏸️"
        next = "⏭️"
        fast_forward = "⏩"
        rewind = "⏪"   
        loop = ["🚫","🔂","🔁"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._queue = []
        self.loop = self.Loop.OFF
        self.vote_skip = True 
        self.votes = set()
        self._now_playing = 0 # Always 0, just to keep consistent with old code

    async def cleanup_and_disconnect(self):
        self.clear_queue()
        if not self.is_connected:
            return

        # Messages deletes
        try:
            await self.queue_message.delete()
        except:
            pass 
        
        try:
            await self.played_message.delete()
        except:
            pass

        try:
            await self.message.delete()
        except:
            pass 
        
        await self.stop()
        await self.disconnect()

    def total_track(self)->int:
        return len(self._queue)

    def current_track(self)->Track:
        if not self.total_track():
            raise Error.QueueIsEmpty
        return self._queue[0]

    def in_queue(self,track_id):
        for track in self._queue:
            if track.get_id() == track_id:
                return True
        return False

    async def add_track(self,track: Track,text_channel: discord.TextChannel):

        if self.in_queue(track.get_id()):
            raise Error.TrackAlreadyInQueue

        self._queue.append(track)
        self.bot = track.bot

        # Send a message in controller channel that shows the Queue
        if not hasattr(self,"queue_message"):
            self.queue_message = await text_channel.send('Chargement de la file...')
        else:
            await self.queue_message.edit(content="",embed = await self.get_queue_embed(), view = self.Page(self))

        # Send a message in controller channel that shows the Controller
        if not hasattr(self,"message"):
            self.message = await text_channel.send('Chargement du player...')
        
        if self.is_playing():
            return
        await self.start_playback(track)

    def clear_queue(self):
        self._queue = []
        self._now_playing = -1


    async def next_track(self):
        await self.stop()

        if self.loop != self.Loop.ONE:
            last_song = self._queue.pop(0)
            if self.loop == self.Loop.ALL:
                self._queue.append(last_song)

        try:
            await self.start_playback(self.current_track())
        except Error.QueueIsEmpty:
            await self.cleanup_and_disconnect()

    async def start_playback(self,track: Track):
        embed = track.get_link_embed(f'En lecture', self.Loop.name[self.loop])
        embed.set_author(name = f"Choisie par : {track.picked_by.display_name}",icon_url=track.picked_by.display_avatar.url)
        self.votes = set()
        view = self.get_view()

        # Play track and set controller message
        await self.message.edit(content="",embed = embed,view = view)
        await self.play(track)
        await self.queue_message.edit(content="",embed = await self.get_queue_embed(), view = self.Page(self,) )

    async def restart_track(self):
        await self.start_playback(self.current_track())

    # UI elements of player controller and queue #
    async def get_queue_embed(self,page = 1):

        embed = discord.Embed(
            title= "Liste de lecture", 
            description=f"Nombre total de pistes: `{self.total_track() - self._now_playing -1}`" , 
            color=0x4287F5)

        if self.total_track() - self._now_playing -1 == 0:
            embed.add_field(name="La liste de lecture est vide", value = "⠀")
        tot = (page-1)*5 + 1 
        for i in range(self._now_playing+tot,self.total_track()):
            if tot>page*5:
                break
            track = self._queue[i]
            embed.add_field(
                name=f"`{tot}` {track.get_title()}" , 
                value = f"Choisie par : {track.picked_by.display_name}",
                inline=False) 
            tot = tot + 1 
        count = (self.total_track() - self._now_playing -1)
        total_page = max(1,(count+4)//5)

        embed.set_footer(text = f"Page {page}/{total_page}")
        return embed

    class View(ui.View):
        def __init__(self,player):
            super().__init__(timeout=None)
            self.player = player

        async def on_error(self, error, item, interaction:discord.Interaction):
            if isinstance(error, Error.NotInCorrectVoiceChannel):
                msg = await interaction.channel.send(f"{interaction.user.mention} Tu dois être dans le canal vocal pour faire ça: `{self.player.channel}`")
                await msg.delete(delay=5)
            else:
                logging.exception(error)
                raise

        class Button(ui.Button):
            def __init__(self,emoji ,row ,callback ,style = discord.ButtonStyle.primary,disabled = False):
                super().__init__(style=style, disabled=disabled, emoji = emoji, row = row)
                self.custom_callback = callback

            async def callback(self,interaction):
                if interaction.user not in self.view.player.channel.members:
                    raise Error.NotInCorrectVoiceChannel

                await self.custom_callback(self,interaction)

    def get_view(self):
        ###                                             ###
        ###             Player Buttons Starts           ###
        ###                                             ###
        view = self.View(self)
        
                    ###         ROW 1           ###

        #Loop Button (All, One, Off)
        async def loop(button,interaction):
            self.loop = (self.loop + 1 )%3
            button.emoji = self.Emoji.loop[(self.loop + 1 )%3]
            embed = self.current_track().get_link_embed('En lecture' , self.Loop.name[self.loop])
            await interaction.response.edit_message(view=button.view , embed = embed)
        view.add_item(self.View.Button(emoji= self.Emoji.loop[(self.loop+1)%3],row = 0,callback= loop))

        #Rewind Button (-10 seconds)
        async def rewind(button,interaction):
            await self.seek(max(0,self.position*1000 - 10000))

        view.add_item(self.View.Button(emoji= self.Emoji.rewind,row = 0,callback= rewind))

        #Play/Pause Buttons
        async def play_button(button: self.View.Button, interaction: discord.Interaction):
            #Pause Audio
            if button.emoji.name == self.Emoji.pause:
                await self.pause()
                button.emoji = self.Emoji.play
            #Resume Audio
            else:
                await self.resume()
                button.emoji = self.Emoji.pause
            await interaction.response.edit_message(view=button.view)

        view.add_item(self.View.Button(emoji= self.Emoji.pause,row = 0,callback= play_button))

        # Fast-Forward Button (+10 seconds)
        async def fast_forward(button,interaction):
            await self.seek(
                min(self.track.length*1000,self.position*1000 + 10000))

        view.add_item(self.View.Button(emoji= self.Emoji.fast_forward,row = 0,callback= fast_forward))

        # Next Track Button
        async def next_track(button,interaction:discord.Interaction):

            allowed_roles = ["DJ"] # Add all the allowed roles here
            user_roles = [role.name for role in interaction.user.roles]
            for role in allowed_roles:
                if role in user_roles:
                    return await self.next_track()

            self.votes.add(interaction.user.id)
            votes = len(self.votes)
            tot = len( [ member for member in self.channel.members if not member.bot] )
            req = (tot+2)//2
            if  req <= votes:
                return await self.next_track()

            track = self._queue[0]
            embed = track.get_link_embed(f'En lecture', self.Loop.name[self.loop] + f" . Votes pour skip {votes}/{req}")
            embed.set_author(name = f"Choisie par : {track.picked_by.display_name}",icon_url=track.picked_by.display_avatar.url)
            await interaction.response.edit_message(embed = embed)
            

        view.add_item(self.View.Button(emoji= self.Emoji.next,row = 0,callback= next_track))
        
        return view

    class Page(ui.View):
        def __init__(self,player,history = False):
            super().__init__(timeout=None)
            self.player = player
            self._page = 1
            self.history = history

            count = self.player._now_playing if history else (self.player.total_track() - self.player._now_playing -1)
            self._total_page = max(1,(count+4)//5)


        async def update(self,interaction):
            if self.history:
                embed = await self.player.get_history_embed(self._page) 
            else:
                embed = await self.player.get_queue_embed(self._page)
            await interaction.response.edit_message(content="",embed = embed,view=self)

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
