import os
import discord
from utils.shards import Bot
from os import environ



bot = Bot(
    command_prefix=environ.get("prefix"), prefix=environ.get('prefix'),
    owner_ids=environ.get('owners'), command_attrs=dict(hidden=True),
    intents=discord.Intents(
        guilds=True, members=True, messages=True, reactions=True, presences=True),allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False)
)
bot.remove_command("help")
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

@bot.event
async def on_command_error(ctx, error):
 await ctx.send(error) # Lazy error_handling, will be changed soon!


bot_token = environ.get('token')
bot.run(bot_token)




