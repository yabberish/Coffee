import discord
from discord.ext import commands
from utils.database import create_tables, sqlite
from utils import default, checks
tables = create_tables.creation(debug=True)


class Setup(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()

  @commands.group(invoke_without_command=True)
  async def setup(self, ctx : commands.Context):
    await ctx.send("**What would you like to setup for the server?**\n\n**`;;setup logs`** - Setup logging for the server.\n**`;;setup starboard <amount_of_stars_to_be_sent>`** - Setup starboard for the server.")  

  @setup.command(
    name = "log",
    help = "Setup the bot for the server.",
    aliases=['logs', 'logging'])
  @commands.has_permissions(manage_guild=True)
  async def logs(self, ctx : commands.Context):
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    logs = await ctx.guild.create_text_channel('coffee-logs', overwrites=overwrites)
    log_channel_id = logs.id
    self.db.execute("INSERT INTO Logging VALUES (?, ?)", (ctx.guild.id, logs.id))
    await ctx.send(f"Successfully setup the server, <#{logs.id}>")
  
  @setup.command()
  @commands.has_permissions(manage_guild=True)
  async def starboard(self, ctx : commands.Context, stars=int(3)):
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    logs = await ctx.guild.create_text_channel('starboard', overwrites=overwrites)
    starboard_channel_id = starboard.id
    self.db.execute("INSERT INTO Starboard VALUES (?, ?, ?)", (ctx.guild.id, starboard.id, stars))
    await ctx.send(f"Successfully setup starboard with a star count of **{stars}**, <#{starboard.id}>")
    




def setup(bot):
 bot.add_cog(Setup(bot))
