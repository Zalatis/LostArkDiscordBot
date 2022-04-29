import spotipy
import wavelink 
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

def checkSpotify(msg: str):
    if "open.spotify.com/track/" in msg:
        link = msg.split("open.spotify.com/track/")[1]
        if len(link) >= 22:
            return link[:22]


def checkYoutube(msg: str):
    if "youtube.com/watch?v=" in msg:
        
        link = msg.split("watch?v=")[1]
        if len(link) >= 11:
            return link[:11]

    if "youtu.be/" in msg:
        link = msg.split("youtu.be/")[1]
        if len(link) >= 11:
            return link[:11]

# Authenticates for spotify api
def authSpotify(bot: commands.Bot):
    if hasattr(bot, "spotify"):
        return bot.spotify

    token = SpotifyClientCredentials(
                    client_id=bot.SPOTIFY_ID,
                    client_secret=bot.SPOTIFY_SECRET, 
            )

    bot.spotify = spotipy.Spotify(auth_manager=token)
    return bot.spotify

async def getSpotifyTrack(bot: commands.Bot,id: str):
    spotify = authSpotify(bot)
    return spotify.track(id)

async def getYoutubeTrack(bot: commands.Bot,id: str):
    tracks = await bot.node.get_tracks(query=id,cls=wavelink.abc.Playable)
    return tracks[0]

async def searchYoutube(bot: commands.Bot, requête: str):
    tracks = await bot.node.get_tracks(query=f"ytsearch:{requête}",cls=wavelink.abc.Playable)
    if not len(tracks):
        return None
    return tracks[0]