import os
import discord

from utils.shards import Bot
from pretty_help import PrettyHelp
from os import environ



bot = Bot(
    command_prefix=environ.get("prefix"), prefix=environ.get('prefix'),
    owner_ids=environ.get('owners'),help_command=PrettyHelp(), command_attrs=dict(hidden=True),
    intents=discord.Intents(
        guilds=True, members=True, messages=True, reactions=True, presences=True
    )
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

print("Ready!")

bot_token = environ.get('token')
bot.run(bot_token)




