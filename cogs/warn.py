import discord
from discord.ext import commands
from datetime import datetime
from utils import checks
from utils.db import create_tables, sqlite
time_format = '%Y-%m-%d %H:%M:%S'
import asyncio

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


class WarnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite.Database()

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx : commands.Context, member : discord.Member, *, reason="None"):
        invoker = ctx.author
        if member.id != ctx.author.id:
            if invoker.top_role > member.top_role:
                self.db.execute("INSERT INTO Warns (user_id, guild_id, reason) VALUES (?, ?, ?)", (member.id, member.guild.id, reason,))
                embed = discord.Embed(
                    description = f"You've been warned in {member.guild.name}\n**Reason:** {reason}\n**Infractor:** {ctx.author.name}",
                    color = 0x2F3136
                )
                await member.send(embed=embed)
                embed = discord.Embed(
                    color = 0x2F3136

                )
                embed.set_author(name=f"✅ Successfully logged a warn with {member.name} for {reason}.", icon_url=str(member.avatar_url))
                await ctx.send(embed=embed)
                author = ctx.author
                guild = ctx.guild
                channel = discord.utils.get(guild.text_channels, name='coffee-logs')
                if channel is None:
                 msg = await ctx.send("Log channel not found, creating one for you...")
                 channel = await guild.create_text_channel('coffee-logs')
                 await asyncio.sleep(2)
                 await msg.edit(content="Adding permissions...")
                 await channel.set_permissions(ctx.guild.default_role, 
                 send_messages=False, read_messages=False)
                 await asyncio.sleep(2)
                 await msg.edit(content="Done! #coffee-logs")
                 await ctx.send("If the channel is not created, please create one manually and add permissions to it.")
                embed = discord.Embed(title="Warn 📝", description=f"**Infractor:** {ctx.author.mention}\n**Reason:** {reason}\n**User warned:**{member.mention}", color=0x2F3136)

                await channel.send(embed=embed)

   """ @commands.command(aliases=['warns', 'infracts'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def infractions(self, ctx, member: discord.Member):
        infracts = self.db.fetchrow("SELECT * FROM Warns WHERE user_id=?, reason=?", (user_id, reason))
        if infracts:
         return infracts["user_id"]
        if ctx.author.id in infracts:
          embed = discord.Embed(
            color=0x2F3136,
            description=f"**<@{user_id}>'s Warnings.\n\n\n{reason}**")
          embed.set_author(name=f"{member.name}'s infractions:", icon_url=str(member.avatar_url))
          await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x2F3136,
            )

            embed.set_author(name=f"{member.name} has no {ctx.invoked_with}!", icon_url=str(member.avatar_url))
            await ctx.send(embed=embed) """
        # TODO: Finish infracts command



                
            



def setup(bot):
    bot.add_cog(WarnCommand(bot))
