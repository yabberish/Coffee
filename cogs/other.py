import discord
from discord.ext import commands
from utils.database import sqlite, create_tables


class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()

  def logs(self, guild_id):
        data = self.db.fetchrow("SELECT * FROM Logging WHERE guild_id=?", (guild_id,))
        if data:
            return data["logs_id"]
        else:
            return None
  
  @commands.Cog.listener()
  async def on_message_delete(self, message):
   log_channel = self.bot.get_channel(self.logs(message.guild.id))
   if log_channel: 
     embed = discord.Embed(
     title="Message Deleted 📝",
     description=f"**Deleted in:** `#{message.channel}`\n**Author:** `{message.author}`\n**Message:** ```{message.content}```",
     color=0x2F3136
     )
     embed.timestamp = message.created_at
     await log_channel.send(embed=embed)
  
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
   log_channel = self.bot.get_channel(self.logs(before.guild.id))
   if before.author.bot is True:
     return None
   if log_channel:
     embed = discord.Embed(
     title="Message Edited 📝",
     description=f"**Edited in:** `#{before.channel}`\n**Author:** `{before.author}`\n**Before:** ```{before.content}```\n**Now:** ```{after.content}```",
     color=0x2F3136
     )
     embed.timestamp = before.created_at
     await log_channel.send(embed=embed)

  

def setup(bot):
  bot.add_cog(Events(bot))

