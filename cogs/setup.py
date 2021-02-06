import discord
from discord.ext import commands
from utils.database import create_tables, sqlite
tables = create_tables.creation(debug=True)

class Setup(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()

  @commands.command(
    name = "setup",
    help = "Setup the bot for the server."
  )
  async def setup_(self, ctx : commands.Context):
    await ctx.guild.create_text_channel('coffee-logs')
    logs = discord.utils.get(ctx.guild.channels, name="coffee-logs")
    await logs.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
    log_channel_id = logs.id
    self.db.execute("INSERT INTO Logging VALUES (?, ?)", (ctx.guild.id, logs.id))
    await ctx.send(f"Successfully setup the server, <#{logs.id}>")

def setup(bot):
 bot.add_cog(Setup(bot))