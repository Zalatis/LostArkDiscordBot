import asyncio, aiohttp, datetime, discord, json, os, time, sys
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import Bot
from cogs import *
from games import *

class LostArkBot():
	"""
	The LostArkBot Class.
	"""

	def __init__(self):
		"""
		Initializes the LostArkBot object.
		"""
		self.game_list = []
		self.add_games()
		self.config = self.get_config()
		self.bot = commands.Bot(command_prefix='!')

	def add_games(self):
		"""
		Adds games objects to self.game_list.
		"""
		self.game_list.append(News())

	def get_config(self):
		"""
		Loads config data from config.json, located in the current working dir.
		If config.json doesn't exist, get_config generates a config.json file with
		data based on the games in self.game_list.
		"""
		try:
			with open("config" + os.sep + "config.json", "r") as jsonFile:
				data = json.load(jsonFile)
			return data
		except FileNotFoundError:
			self.generate_config()
			with open("config" + os.sep + "config.json", "r") as jsonFile:
				data = json.load(jsonFile)
			return data

	def generate_config(self):
		"""
		Generates a config.json file for first use of bot or if config.json was
		deleted.
		"""
		data = {}
		data["games"] = {}
		for game in self.game_list:
			data["games"][game.name] = {}
			data["games"][game.name]["channels"] = [""]
		# TODO: Needs to handle permissions error.
		with open(os.path.dirname(os.path.realpath(__file__)) +  os.sep + "config" + os.sep + "config.json", "w") as jsonFile:
			json.dump(data, jsonFile, indent=4)

	def reinitialize_config(self):
		"""
		Reloads config data from config.json.
		"""
		with open("config" + os.sep + "config.json", "r") as jsonFile:
			data = json.load(jsonFile)
		self.config = data

	def get_updated_games(self):
		"""
		Returns a list of game objects whos current news title doesn't match their
		new news title after updating their news information.
		"""
		updated_game_list = []
		for game in self.game_list:
			print("Reinitializing " + game.name)
			current_news_title = game.news["title"]
			try:
				game.get_news_info()
			except Exception as e:
				print("Error reinitializing " + game.name + ": " + str(e))
			else:
				if current_news_title != game.news["title"]:
					updated_game_list.append(game)
		print("\nReinitialized Games\n")
		return updated_game_list

	def get_channel_games(self, channel):
		"""
		Returns a list of games that the specified channel is subscribed to.
		"Subscribed" meaning the channel name is within a list of channel names
		under the game name in config.json.
		"""
		game_list = []
		for game in self.game_list:
			for channel_name in self.config['games'][game.name]['channels']:
				if channel_name == channel.name:
					game_list.append(game)
		return game_list

	def get_game_channels(self, game):
		"""
		Returns a list of channels that are subscribed to a specified game.
		"Subscribed" meaning the channel name is within a list of channel names
		under the game name in config.json.
		"""
		channel_list = []
		for channel in self.bot.get_all_channels():
			for channel_name in self.config['games'][game.name]['channels']:
				if channel_name == channel.name:
					channel_list.append(channel)
		return channel_list

	def initialize_news(self):
		"""
		Initializes all Game objects in self.game_list by calling their
		get_news_info function.
		"""
		print("Initializing Games:\n")
		for game in self.game_list:
			try:
				game.get_news_info()
			except Exception as e:
				print (game.name + " error initializing: " + str(e))
			else:
				print(game.name + " initialized.")
		print("\nDone Initializing\n")

	def get_news_message(self, game):
		"""
		Returns a discord embed object that contains the news message for the
		specified game.
		A news message must at least have a title and a link and the news
		description should not exceed 400 characters.
		"""
		embed = discord.Embed()
		if game.news["title"] is None or game.news["url"] is None:
			embed.title = "Error occurred when retrieving " + game.name + " news notes"
			return embed
		embed.title = game.news["title"]
		embed.url = game.news["url"]
		if game.news["desc"] is not None:
			desc = ""
			game_strings = game.news["desc"].split("\n")
			for string in game_strings:
				desc = desc + string + "\n"
				if len(desc) > 400:
					desc = desc + "..."
					break
			embed.description = desc
		if game.color is not None:
			embed.color = game.color
		if game.thumbnail is not None:
			embed.set_thumbnail(url=game.thumbnail)
		if game.news["image"] is not None:
			embed.set_image(url=game.news["image"])
		return embed

	def get_embed_message(self):
		"""
		Returns a discord embed object that contains about information about LostArkBot.
		"""
		embed_message = discord.Embed()
		embed_message.title = 'Zalati\'s LostArkBot'
		embed_message.color = 16200039
		embed_message.description = 'LostArkBot delivers news on demand and when they pop up.'
		embed_message.add_field(name='Commands', value="!news -> Displays game news.\n!LostArkBot reload -> Reloads config.", inline=False)
		embed_message.add_field(name='Source', value='https://github.com/Zalatis/LostArkDiscordBot', inline=False)
		embed_message.set_image(url='https://assets.maxroll.gg/wordpress/Lost_Ark_banner_1-1024x341.jpg')
		embed_message.set_thumbnail(url='https://d1glcu56fxkf6q.cloudfront.net/statics/2022-02-25/images/LostArkIcon.png')
		embed_message.set_footer(text = 'Developer: Zalati#5367 based on kenreidwilson work')
		return embed_message

lostarkbot = LostArkBot()

def main():
	"""
	Initializes news information and starts the bot.
	"""
	while True:
		try:
			push_game_updates_task = asyncio.ensure_future(push_game_updates())
			lostarkbot.bot.loop.run_until_complete(lostarkbot.bot.start(sys.argv[1]))
		except aiohttp.client_exceptions.ClientConnectorError:
			print("Could not connect to Discord, reconnecting...")
			push_game_updates_task.cancel()
			time.sleep(10)
		except IndexError:
			print("You must enter a bot token.")
			print("Usage: python3 main.py <bot-token>")
			push_game_updates_task.cancel()
			sys.exit(1)
		except discord.errors.LoginFailure:
			print("Discord login failed: Invalid bot token.")
			push_game_updates_task.cancel()
			sys.exit(1)
		except KeyboardInterrupt:
			print("\nExitting Gracefully")
			push_game_updates_task.cancel()
			lostarkbot.bot.loop.run_until_complete(lostarkbot.bot.close())
			sys.exit(0)

async def push_game_updates():
	"""
	Checks if a news has been released for all games in lostarkbot.game_list.
	Every 5 minutes, all games update their news information and games with new
	news have their embed news message pushed to their subscribed channels.
	"""
	await lostarkbot.bot.wait_until_ready()
	while True:
		await asyncio.sleep(300)
		print("\nReinitializing Games\n")
		for game in lostarkbot.get_updated_games():
			try:
				for channel in lostarkbot.get_game_channels(game):
					await channel.send(embed=lostarkbot.get_news_message(game))
			except (discord.DiscordException, discord.ClientException, discord.HTTPException, discord.NotFound):
				print("Could not connect to Discord when displaying " + game.name + " new news information.")

@lostarkbot.bot.event
async def on_message(message):
	"""
	Handles LostArkBot commands sent as messages on a discord server.
	"""

	if message.content == '!news':
		"""
		Handles !news command.
		Sends current news information, for all games the channel is subscribed to,
		to the channel that the message came from.
		"""
		channel_games = lostarkbot.get_channel_games(message.channel)
		if len(channel_games) == 0:
			await message.channel.send(message.channel.name + " is not subscribed to any games.")
		else:
			for game in channel_games:
				await message.channel.send(embed=lostarkbot.get_news_message(game))

	if message.content.startswith('!news '):
		"""
		Handles !news command for a specific game.
		Sends current news information, for the game specified after !news, to
		the channel that the message came from.
		"""
		for game in lostarkbot.game_list:
			if message.content[7:].lower() in game.names:
				await message.channel.send(embed=lostarkbot.get_news_message(game))
				return
		await message.channel.send("Could not find news info for " + message.content[7:].lower())

	if message.content == '!lostarkbot':
		"""
		Handles !lostarkbot command.
		Sends lostarkbot's embed about message to the channel that the message came
		from.
		"""
		await message.channel.send(embed=lostarkbot.get_embed_message())

	if message.content.startswith('!newsbot '):
		"""
		Handles !lostarkbot reload command.
		Reloads lostarkbot.data with data from config.json.
		"""
		if 'reload' in message.content:
			lostarkbot.reinitialize_config()
			await message.channel.send("Reinitialized config.json")

@lostarkbot.bot.event
async def on_ready():
	"""
	Handles when LostArkBot is ready.
	"""
	print(lostarkbot.bot.user.name + " is online.\n")
	lostarkbot.initialize_news()
	# TODO: Presence not showing.
	await lostarkbot.bot.change_presence(activity=discord.Activity(game=discord.Game(name="LostArkBot | !lostarkbot")))

if __name__ == '__main__':
	main()
