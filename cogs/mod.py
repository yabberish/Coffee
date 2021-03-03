import discord
import re
import asyncio
from discord.ext import commands
from utils import checks, default
from utils.database import sqlite, create_tables



# https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
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
        self.db = sqlite.Database()
    
    def logs(self, guild_id):
        data = self.db.fetchrow("SELECT * FROM Logging WHERE guild_id=?", (guild_id,))
        if data:
            return data["logs_id"]
        else:
            return None

    @commands.command(
      name="kick",
      help="Kick a user from the server."
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
            color = 0x2F3136
          )
          embed.set_footer(text=f"Command invoked by {ctx.author}")
          embed.set_author(name=f"✅ {member.name} has been kicked from the server", icon_url=member.avatar_url)
          await ctx.send(embed=embed)
          await member.send(f"You've been kicked from **{ctx.guild.name}** for **{reason}** by **{ctx.author}**")

          log_channel = self.bot.get_channel(self.logs(ctx.guild.id))
          if log_channel:
            embed = discord.Embed(
              title="Kick 📝",
              description=f"**User Kicked:** `{member}`\n**Moderator:** `{ctx.author}`\n**Reason:** `{reason}`",
              color=0x2F3136
            )
          await log_channel.send(embed=embed)

      except Exception as e:
          await ctx.send(e)

    @commands.command(
      name="ban",
      help="Ban a user from the server."
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
            color = 0x2F3136
          )
          embed.set_footer(text=f"Command invoked by {ctx.author}")
          embed.set_author(name=f"✅ {member.name} has been banned from the server", icon_url=member.avatar_url)
          await ctx.send(embed=embed)
          await member.send(f"You've been banned from **{ctx.guild.name}** for **{reason}** by **{ctx.author}**")

          log_channel = self.bot.get_channel(self.logs(ctx.guild.id))
          if log_channel:
            embed = discord.Embed(
              title="Ban 📝",
              description=f"**User banned:** `{member}`\n**Moderator:** `{ctx.author}`\n**Reason:** `{reason}`",
              color=0x2F3136
            )
          await log_channel.send(embed=embed)

      except Exception as e:
          await ctx.send(e)
    
    @commands.command(
      name="unban",
      help="Unban a user from your server."
    )
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def unban_(self, ctx, member: MemberID, *, reason: str = None):
        """ Unban a user. """
        try:
            await ctx.guild.unban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
            embed = discord.Embed(
              color=0x2F3136
            )
            embed.set_footer(text=f"Command invoked by {ctx.author}")
            embed.set_author(name=f"✅ Unbanned!")
            await ctx.send(embed=embed)

            log_channel = self.bot.get_channel(self.logs(ctx.guild.id))
            if log_channel:
              embed = discord.Embed(
               title="Unban 📝",
               description=f"**User unbanned:** `{member}`\n**Moderator:** `{ctx.author}`\n**Reason:** `{reason}`",
               color=0x2F3136
             )
            await log_channel.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @command.command(aliases = ["clear"], help = "Clear a x amount of messages in chat.")
    @commands.max_concurrency(1, per=commands.BucketType.guild)
    @permissions.has_permissions(manage_messages=True)
    async def purge(self, ctx):
    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None, message=True):
        if limit > 2000:
            return await ctx.send(f'Too many messages to search given ({limit}/2000)')

        if not before:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.Forbidden:
            return await ctx.send('I do not have permissions to delete messages.')
        except discord.HTTPException as e:
            return await ctx.send(f'Error: {e} (try a smaller search?)')


        deleted = len(deleted)
        transcript = await chat_exporter.export(ctx.channel, limit=deleted, tz_info)
            transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"coffee-transcript-{ctx.channel.name}.html")
        if message is True:
            embed = discord.Embed(color = 0x2F3136)
            embed.set_author(name = f"✅ Successfully pruned {deleted} messages.")
            embed.set_footer(text=f"Command invoked by {ctx.author}")
            await ctx.send(embed=embed)

           log_channel = self.bot.get_channel(self.logs(ctx.guild.id))
           if log_channel:
             embed = discord.Embed(
               title="Unban 📝",
               description=f"**Messages deleted:** `{deleted}`\n**Moderator:** {ctx.author}\n**Channel Transcript:**`",
               color=0x2F3136)
            await log_channel.send(embed=embed)
            await asyncio.sleep(2)
            await log_channel.send(file=transcript_file)
    
    


def setup(bot):
    bot.add_cog(Moderation(bot))
