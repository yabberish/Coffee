from templatebot import Bot
from discord import AllowedMentions, Activity, Game
from os import environ as env
from dotenv import load_dotenv
import discord
from discord.ext import fancyhelp


bot = Bot(
    name="Coffee",
    command_prefix=";;",
    allowed_mentions=AllowedMentions(
        everyone=False, roles=False, users=True
    ),
    help_command=fancyhelp.EmbeddedHelpCommand(color=0x73D3B3),
    activity=Game("with logs 📝"),
)

bot.VERSION = "2.0.0"

bot.load_initial_cogs(
    "cogs.logs", "cogs.mod", "cogs.setup", "cogs.top-gg"
)

@bot.event
async def on_command_error(ctx, error):
 await ctx.send(f"💥 {error}")
  # Lazy error_handling, will be changed soon!


bot.run(env.get("TOKEN", None))
