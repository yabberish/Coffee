import discord
import re
import asyncio

from discord.ext import commands
from utils import checks, default







# https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py <--- Source
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"Member {argument} does not exist.") from None
        else:
            return m.id


class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason that is being inputted is too long ({len(argument)}/{reason_max})')
        return ret


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
      name="kick",
      help="Kick a user from the server!",
      usage="@bob#8819 posting memes in general"
    )
    @commands.guild_only()
    @checks.has_permissions(kick_members=True)
    async def kick_(self, ctx : commands.Context, member: discord.Member, *,   reason: str = None):
      """ Kicks a user from the server. """
      if await checks.check_priv(ctx, member):
             return
      try:
          await member.kick(reason=default.responsible(ctx.author, reason))
          embed = discord.Embed(
            title = "👟",
            description = f"**{member.name}#{member.discriminator}** Has been kicked from the server for **{reason}**",
            color = 0x2F3136
          )
          embed.set_footer(text=f"Command invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
          embed.set_author(icon_url=member.avatar_url)
          await ctx.send(content="✅", embed=embed)
      except Exception as e:
          await ctx.send(e)
    
    @commands.command(
      name="ban",
      help="Permanently ban a user from the server.",
      usage="@bob#8819 posting not safe for work content."
    )
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def banish(self, ctx : commands.Context, member: discord.Member, *,   reason: str = None):
      """ Bans a user from the server. """
      if await checks.check_priv(ctx, member):
             return
      try:
          await member.ban(reason=default.responsible(ctx.author, reason))
          embed = discord.Embed(
            title = "🔨",
            description = f"**{member.name}#{member.discriminator}** Has been banned from the server for **{reason}",
            color = 0x2F3136
          )
          embed.set_footer(text=f"Command invoked by {ctx.author.name}")
          embed.set_thumbnail(url=member.avatar_url)
          await ctx.send(content="✅", embed=embed)
      except Exception as e:
          await ctx.send(e)
    
    @commands.guild_only()
    @checks.has_permissions(kick_members=True)
    async def banish(self, ctx : commands.Context, member: discord.Member, *,   reason: str = None):
      """ Bans a user from the server. """
      if await checks.check_priv(ctx, member):
             return
      try:
          await member.ban(reason=default.responsible(ctx.author, reason))
          embed = discord.Embed(
            title = "🔨",
            description = f"**{member.name}#{member.discriminator}** Has been banned from the server for **{reason}",
            color = 0x2F3136
          )
          embed.set_footer(text=f"Command invoked by {ctx.author.name}")
          embed.set_thumbnail(url=member.avatar_url)
          await ctx.send(content="✅", embed=embed)
      except Exception as e:
          await ctx.send(e)

    

# TODO: add logging context


def setup(bot):
    bot.add_cog(Moderation(bot))
