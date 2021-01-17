import discord
import re
import asyncio

from discord.ext import commands
from utils import checks

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


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
      name="kick",
      description="Kick a user from the server!",
      usage="@bob#8819 posting memes in general"
    )
    @commands.guild_only()
    @checks.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,   reason: str = None):
      """ Kicks a user. """
      if await checks.check_priv(ctx, member):
             return

      try:
          await member.kick(reason=default.responsible(ctx.author, reason))
          await ctx.send(default.actionmessage("Kicked."))
      except Exception as e:
          await ctx.send(e)



def setup(bot):
    bot.add_cog(Mod(bot))