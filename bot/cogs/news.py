import discord
from discord.ext import commands,tasks
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class LostArkNews(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.name = "Lost Ark News"
        self.news = {"title": None, "url": None, "desc": None, "image": None}
        self.thumbnail = ""
        self.color = 30070
        self.update_news.start()
        self.last_news_title = None
        self.last_news_description = None
        self.last_news_message_id = None
        self.msg = None

    def cog_unload(self):
        self.update_news.cancel()

    def get_news_info(self):
        # Gets source of Latest official news.
        try:
            request = Request("https://www.playlostark.com/fr-fr/news", headers={'User-Agent': 'Mozilla/5.0'})
            source = urlopen(request).read()
        except:
            raise Exception("Couldn't connect to " + self.name + "' website.")

        try:
            news_divs = soup(source, "html.parser").findAll("div",{"class":"ags-SlotModule ags-SlotModule--blog ags-SlotModule--threePerRow"})
        except:
            raise Exception("Error retrieving news_divs")

        # Gets Lost Ark news url.
        try:
            self.news["url"] = "https://www.playlostark.com" + news_divs[0].a["href"]
            if self.news["url"] is None:
                raise Exception("Could not find " + self.name + " url.")
            # print("url = " + self.news["url"])
        except:
            raise Exception("Error retrieving " + self.name + " url. 1")

        # Gets Lost Ark news title.
        try:
            news_title = soup(source, "html.parser").find("span",{"class":"ags-SlotModule-contentContainer-heading ags-SlotModule-contentContainer-heading ags-SlotModule-contentContainer-heading--blog"})
            self.news["title"] = news_title.find(text=True)
            if self.news["title"] is None:
                raise Exception("Could not find " + self.name + " title.")
            # print("title = " + self.news["title"])
        except:
            raise Exception("Error retrieving " + self.name + " title.")

        # Gets Lost Ark news description.
        try:
            news_description = soup(source, "html.parser").find("div",{"class":"ags-SlotModule-contentContainer-text ags-SlotModule-contentContainer-text--blog ags-SlotModule-contentContainer-text"})
            self.news["desc"] = news_description.find(text=True)
            if self.news["desc"] is None:
                raise Exception("Could not find " + self.name + " description.")
            if len(self.news["desc"]) > 400:
                self.news["desc"] = self.news["desc"][:400] + "..."
            # print("desc = " + self.news["desc"])
        except:
            raise Exception("Error retrieving " + self.name + " description.")

        # Gets Lost Ark news image.
        try:
            self.news["image"] = "https:" + soup(source, "html.parser").find("img",{"class":"ags-SlotModule-imageContainer-image"})["src"]
            if self.news["image"] is None:
                raise Exception("Could not find " + self.name + " image url.")
            # print("image = " + self.news["image"])
        except:
            raise Exception("Error retrieving " + self.name + " image url.")  
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
        self.image = self.news["image"].strip()
        try:
            with open ('./bot/cogs/txt_files/latest-news.txt', 'r+', encoding='utf8') as f:
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
            raise Exception("Impossible d'ouvrir latest-news.txt")
        # Not same title
        if self.last_news_title != self.title:
            embed = discord.Embed(title=self.title, url=self.url, description=self.desc, color=self.color)
            embed.set_image(url=self.news["image"])
            msg = await self.news_channel.send(embed=embed)
            self.last_news_message_id = msg.id
            try:
                with open ('./bot/cogs/txt_files/latest-news.txt', 'w+', encoding='utf8') as f:
                    f.seek(0)
                    f.truncate()
                    f.write("Latest Title : " + self.title + "\nLatest Description : " + repr(self.desc) + "\nMessage ID : " + str(self.last_news_message_id))
                    f.close()
            except:
                raise Exception("Impossible d'ouvrir latest-news.txt")
        # Same Title but not same post content
        elif (self.last_news_title == self.title) and (self.last_news_description != repr(self.desc)):
            try:
                with open ('./bot/cogs/txt_files/latest-news.txt', 'w+', encoding='utf8') as f:
                    f.seek(0)
                    f.truncate()
                    f.write("Latest Title : " + self.title + "\nLatest Description : " + repr(self.desc) + "\nMessage ID : " + str(self.last_news_message_id))
                    f.close()
            except:
                raise Exception("Impossible d'ouvrir latest-news.txt")
            self.msg = await self.news_channel.fetch_message(int(self.last_news_message_id))
            embed = discord.Embed(title=self.title, url=self.url, description=self.desc, color=self.color)
            embed.set_image(url=self.news["image"])
            await self.msg.edit(embed = embed)

def setup(bot:commands.Bot):
    bot.add_cog(LostArkNews(bot))
