import discord
from discord.ext import commands,tasks
import re
import httpx

class LostArkForumNews(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.name = "Lost Ark Forum"
        self.news = {"title": None, "url": None, "desc": None, "image": None}
        self.thumbnail = ""
        self.color = 1179867
        self.update_news.start()
        self.last_news_title = None
        self.last_news_post_content = None
        self.last_news_message_id = None
        self.msg = None

    def cog_unload(self):
        self.update_news.cancel()

    def get_news_info(self):
        # Gets source of Latest official news from Forum.
        try:
            url = (
                "https://forums.playlostark.com/c/official-news/annonces-officielles-et-evenements/18/l/latest.json?ascending=false"
                )
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            }
            response = httpx.get(url, headers=headers)
            apiResponse = response.json()
            base = apiResponse["topic_list"]["topics"]

            self.api = []
            loop = 1
            for each in base:
                if loop != 0:
                    # print(each)
                    post_id = each["id"]
                    clean_url = f"https://forums.playlostark.com/t/{post_id}.json"
                    response = httpx.get(clean_url, headers=headers)
                    responseJSON = response.json()

                    title = responseJSON["title"]
                    created_at = responseJSON["created_at"]
                    # grab last message in post
                    post_content = responseJSON["post_stream"]["posts"][-1]["cooked"]
                    # # Double new lines from post content
                    # post_content = re.sub(r"\n", "\n\n", post_content)
                    # replace li and ul elements
                    post_content = re.sub(r"<ul>\n", "", post_content)
                    post_content = re.sub(r"<ol>\n", "", post_content)
                    post_content = re.sub(r"<li>", "• ", post_content)
                    post_content = re.sub(r"<\/li>\n", "\n", post_content)
                    # remove html tags from post content
                    post_content = re.sub(r"<[^\/].*?>", "", post_content)
                    post_content = re.sub(r"<\/.*?>", "\n", post_content)
                    # remove extra spaces from post content
                    # post_content = re.sub(r"\s{2,}", " ", post_content)
                    # last message in post content

                    # check if post is pinned
                    pinned = responseJSON["pinned"]
                    staff = responseJSON["post_stream"]["posts"][0]["staff"]

                    # author of post
                    author = responseJSON["post_stream"]["posts"][0]["username"]

                    # url to post
                    slug = responseJSON["slug"]
                    url = f"https://forums.playlostark.com/t/{slug}/{post_id}"
                    if len(post_content) > 1500:
                        post_content = post_content[:1500] + "..."

                    if not pinned and staff:
                        self.api.append(
                            {
                                "title": title,
                                "created_at": created_at,
                                "post_content": post_content,
                                "author": author,
                                "url": url
                            }
                        )
                        loop = 0

            self.title = self.api[0]["title"]
            self.created_at = self.api[0]["created_at"]
            self.post_content = self.api[0]["post_content"]
            self.url = self.api[0]["url"]
            self.author = self.api[0]["author"]

            return self
        except Exception as e:
            print("Error while trying to get_news_info: ", e)

    # Updates Lost Ark news every 5 minutes.
    @tasks.loop(minutes=5)
    async def update_news(self):
        await self.bot.wait_until_ready()
        self.get_news_info()
        self.news_channel = await self.bot.fetch_channel(int(self.bot.NEWS_CHANNEL_ID))
        try:
            with open ('./bot/cogs/txt_files/latest-news.txt', 'r', encoding='utf8') as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if line.startswith("Latest Title : "):
                        self.last_news_title = line.split("Latest Title : ")[1].strip()
                    elif line.startswith("Latest Description : "):
                        self.last_news_post_content = None
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
                            self.last_news_post_content = line.split("Latest Description : ")[1].strip()
                        elif line.startswith("Message ID : "):
                            self.last_news_message_id = line.split("Message ID : ")[1].strip()
                        else:
                            f.truncate()
                            self.last_news_title = None
                            self.last_news_post_content = None
                            self.last_news_message_id = None
                    f.close()
            except:
                raise Exception("Impossible d'ouvrir latest-forum-news.txt")
            if self.last_news_title != None:
                if self.last_news_title != self.title:
                    # print("Le titre a changé")
                    embed = discord.Embed(title=self.title, url=self.url, description=self.post_content, color=self.color)
                    msg = await self.news_channel.send(embed=embed)
                    self.last_news_message_id = msg.id
                    try:
                        with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'w+', encoding='utf8') as f:
                            f.seek(0)
                            f.truncate()
                            f.write("Latest Title : " + self.title + "\nLatest Description : " + repr(self.post_content) + "\nMessage ID : " + str(self.last_news_message_id))
                            f.close()
                    except:
                        raise Exception("Impossible d'ouvrir latest-forum-news.txt")
                elif self.last_news_title == self.title and repr(self.last_news_post_content) != repr(self.post_content):
                    try:
                        with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'w+', encoding='utf8') as f:
                            f.seek(0)
                            f.truncate()
                            f.write("Latest Title : " + self.title + "\nLatest Description : " + repr(self.post_content) + "\nMessage ID : " + str(self.last_news_message_id))
                            f.close()
                    except:
                        raise Exception("Impossible d'ouvrir latest-forum-news.txt")
                    self.msg = await self.news_channel.fetch_message(int(self.last_news_message_id))
                    embed = discord.Embed(title=self.title, url=self.url, description=self.post_content, color=self.color)
                    await self.msg.edit(embed = embed)
            else:
                # print("Premier message")
                embed = discord.Embed(title=self.title, url=self.url, description=self.post_content, color=self.color)
                msg = await self.news_channel.send(embed=embed)
                self.last_news_message_id = msg.id
                try:
                    with open ('./bot/cogs/txt_files/latest-forum-news.txt', 'w+', encoding='utf8') as f:
                        f.seek(0)
                        f.truncate()
                        f.write("Latest Title : " + self.title + "\nLatest Description : " + repr(self.post_content) + "\nMessage ID : " + str(self.last_news_message_id))
                        f.close()
                except:
                    raise Exception("Impossible d'ouvrir latest-forum-news.txt")

def setup(bot:commands.Bot):
    bot.add_cog(LostArkForumNews(bot))
