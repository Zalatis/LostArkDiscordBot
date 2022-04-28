import discord
from discord.ext import commands
from discord import ui
import wavelink
import logging
from datetime import datetime


def formatTime(timeInMiliSecond: str):
    seconds = timeInMiliSecond//1000
    if seconds>=3600:
        return datetime.strftime(datetime.fromtimestamp(seconds),"%H:%M:%S")
    return datetime.strftime(datetime.fromtimestamp(seconds), "%M:%S")

# Makes text in block format for embed
def formatText(text: str):
        return f"`{text}`"

# Keeps information about a song
class Track(wavelink.YouTubeTrack):

    def __init__(self, bot: commands.Bot, author: discord.User , youtubeTrack: wavelink.abc.Playable):
        self.bot = bot
        self.picked_by = author

        # Process Youtube
        self.youtubeTrack = youtubeTrack 
        super().__init__(youtubeTrack.id, youtubeTrack.info)
        self.thumbnail_url = f"https://img.youtube.com/vi/{self.identifier}/default.jpg"

    def __str__(self) -> str:
        return self.get_title()

    def get_title(self):
        return self.title

    def get_id(self):
        yt = self.identifier

        return yt

    # get the embed (Block Text) for the song
    def get_link_embed(self, title="Chanson ajoutée" , loop: str = "OFF"):
        embed = discord.Embed(title=title, color=0x4287F5)
        embed.description = self.get_title()
        embed.set_thumbnail(url=str(self.thumbnail_url))

        embed.add_field(
            name="Artiste",
            value=formatText(self.author),
            inline=True
        )

        embed.add_field(
            name="Durée",
            value=formatText(formatTime(self.duration*1000)),
            inline=True
        )

        embed.set_footer(text=f"En boucle: {loop}")

        return embed
