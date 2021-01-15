import discord
from discord.ext import commands
import sqlite3
from datetime import datetime
conn = sqlite3.connect('database/database.db')
time_format = '%Y-%m-%d %H:%M:%S'

def pretty_date(time=False):
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return 'Unknown.'

    if day_diff == 0:
        if second_diff < 10:
            return "Just now"
        if second_diff < 60:
            return str(round(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "A minute ago"
        if second_diff < 3600:
            return str(round(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "An hour ago"
        if second_diff < 86400:
            return str(round(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(round(day_diff)) + " days ago"
    if day_diff == 7 and day_diff < 13:
        return str(round(day_diff / 7)) + " week ago"
    if day_diff < 31:
        return str(round(day_diff / 7)) + " weeks ago"
    if day_diff > 28 and day_diff < 60:
        return str(round(day_diff / 30)) + " month ago"
    if day_diff > 60 and day_diff < 365:
        return str(round(day_diff / 30)) + " months ago"
    return str(round(day_diff / 365)) + " years ago"


c = conn.cursor()

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member : discord.Member, *, reason="None given."):
        invoker = ctx.author
        if member.id != ctx.author.id:
            if invoker.top_role > member.top_role:
                c.execute("INSERT INTO warns (user_id, guild_id, reason) VALUES (?, ?, ?)", (member.id, member.guild.id, reason,))
                conn.commit()
                embed = discord.Embed(
                    description = f"You've been warned in {member.guild.name}\**Reason:** {reason}\n**Infractor:** {ctx.author.name}",
                    color = 0x2F3136
                )
                await member.send(embed=embed)
                embed = discord.Embed(
                    color = 0x2F3136

                )
                embed.set_author(name=f"✅ Successfully warned & messaged {member.name.discriminator} for {reason}.", icon_url=str(member.avatar_url))
                await ctx.send(embed=embed)
            



def setup(bot):
    bot.add_cog(Warn(bot))
