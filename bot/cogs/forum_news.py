from turtle import pos
import discord
from discord.ext import commands,tasks
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class LostArkForumNews(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.name = "Lost Ark Forum"
        self.news = {"title": None, "url": None, "desc": None, "image": None}
        self.thumbnail = ""
        self.color = 1179867
        self.update_news.start()
        self.last_news_title = None
        self.last_news_description = None
        self.last_news_message_id = None
        self.msg = None

    def cog_unload(self):
        self.update_news.cancel()

    def get_news_info(self):
        # Gets source of Latest official news from Forum.
        try:
            request = Request("https://forums.playlostark.com/c/official-news/annonces-officielles-et-evenements/18", headers={'User-Agent': 'Mozilla/5.0'})
            source = urlopen(request).read()
        except:
            raise Exception("Couldn't connect to " + self.name + "' website.")

        try:
            news_span = soup(source, "html.parser").findAll("span",{"class":"link-top-line"})
        except:
            raise Exception("Error retrieving news_span")

        # Gets Lost Ark news url.
        try:
            self.news["url"] = news_span[0].a["href"]
            if self.news["url"] is None:
                raise Exception("Could not find " + self.name + " url.")
        except:
            raise Exception("Error retrieving " + self.name + " url. 1")

        # Gets Lost Ark news title.
        try:
            news_title = soup(source, "html.parser").find("a",{"class":"title raw-link raw-topic-link"})
            self.news["title"] = news_title.find(text=True)
            if self.news["title"] is None:
                raise Exception("Could not find " + self.name + " title.")
        except:
            raise Exception("Error retrieving " + self.name + " title.")

        # Gets Lost Ark news description
        try:
            request = Request(self.news["url"], headers={'User-Agent': 'Mozilla/5.0'})
            source = urlopen(request).read()
            forum_post = soup(source, "html.parser").find_all("div",{"class":"post"})[-1].getText()
            post_text = forum_post.replace("\n", " ")
            self.news["desc"] = post_text
            if self.news["desc"] is None:
                raise Exception("Could not find " + self.name + " description.")
            if len(self.news["desc"]) > 400:
                self.news["desc"] = self.news["desc"][:400] + "..."
        except:
            raise Exception("Error retrieving " + self.name + " description.")
        return self

    # Updates Lost Ark news every 5 minutes.
    @tasks.loop(minutes=5)
    async def update_news(self):
        await self.bot.wait_until_ready()
        self.get_news_info()
        self.news_channel = await self.bot.fetch_channel(int(self.bot.NEWS_CHANNEL_ID))
        self.title = self.news["title"].strip()
        self.url = self.news["url"].strip()
        self.desc = self.news["desc"].strip()
        try:
            with open ('./bot/cogs/txt_files/latest-news.txt', 'r', encoding='utf8') as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if line.startswith("Latest Title : "):
                        self.last_news_title = line.split("Latest Title : ")[1].strip()
                    elif line.startswith("Latest Description : "):
                        self.last_news_description = None
                    elif line.startswith("Message ID : "):
                        self.last_news_message_id = None
                    else:
                        self.last_news_title = None
                f.close()
        except:
            raise Exception("Impossible d'ouvrir latest-forum-news.txt")
        if self.last_news_title != self.title:
            try:
                with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'r+', encoding='utf8') as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if line.startswith("Latest Title : "):
                            self.last_news_title = line.split("Latest Title : ")[1].strip()
                        elif line.startswith("Latest Description : "):
                            self.last_news_description = line.split("Latest Description : ")[1].strip()
                        elif line.startswith("Message ID : "):
                            self.last_news_message_id = line.split("Message ID : ")[1].strip()
                        else:
                            f.truncate()
                            self.last_news_title = None
                            self.last_news_description = None
                            self.last_news_message_id = None
                    f.close()
            except:
                raise Exception("Impossible d'ouvrir latest-forum-news.txt")
            if self.last_news_title != None:
                if self.last_news_title != self.title:
                    # print("Le titre a changé")
                    embed = discord.Embed(title=self.title, url=self.url, description=self.desc, color=self.color)
                    msg = await self.news_channel.send(embed=embed)
                    self.last_news_message_id = msg.id
                    try:
                        with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'w+', encoding='utf8') as f:
                            f.seek(0)
                            f.truncate()
                            f.write("Latest Title : " + self.title + "\nLatest Description : " + self.desc + "\nMessage ID : " + str(self.last_news_message_id))
                            f.close()
                    except:
                        raise Exception("Impossible d'ouvrir latest-forum-news.txt")
                elif self.last_news_title == self.title and self.last_news_description != self.desc:
                    # print("La description a changé")
                    try:
                        with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'w+', encoding='utf8') as f:
                            f.seek(0)
                            f.truncate()
                            f.write("Latest Title : " + self.title + "\nLatest Description : " + self.desc + "\nMessage ID : " + str(self.last_news_message_id))
                            f.close()
                    except:
                        raise Exception("Impossible d'ouvrir latest-forum-news.txt")
                    self.msg = await self.news_channel.fetch_message(int(self.last_news_message_id))
                    embed = discord.Embed(title=self.title, url=self.url, description=self.desc, color=self.color)
                    await self.msg.edit(embed = embed)
            else:
                # print("Premier message")
                embed = discord.Embed(title=self.title, url=self.url, description=self.desc, color=self.color)
                msg = await self.news_channel.send(embed=embed)
                self.last_news_message_id = msg.id
                try:
                    with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'w+', encoding='utf8') as f:
                        f.seek(0)
                        f.truncate()
                        f.write("Latest Title : " + self.title + "\nLatest Description : " + self.desc + "\nMessage ID : " + str(self.last_news_message_id))
                        f.close()
                except:
                    raise Exception("Impossible d'ouvrir latest-forum-news.txt")

def setup(bot:commands.Bot):
    bot.add_cog(LostArkForumNews(bot))
