import discord
from discord.ext import commands
from os import environ

owners = [738604939957239930]


def is_owner(ctx):
    return ctx.author.id in owners


async def check_permissions(ctx, perms, *, check=all):
    if ctx.author.id in owners:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)


async def check_priv(ctx, member):
    try:
        if member == ctx.author:
            await ctx.send(f"You've played yourself... oh wait")
        if member.id == ctx.bot.user.id:
            await ctx.send("Why do you hate me so much...")

        if ctx.author.id == ctx.guild.owner.id:
            return False

        if member.id in owners:
            if ctx.author.id not in owners:
                await ctx.send(f"I can't {ctx.command.name} a bot developer...")
            else:
                pass
        if member.id == ctx.guild.owner.id:
            await ctx.send(f"You can't {ctx.command.name} the server owner.")
        if ctx.author.top_role == member.top_role:
            await ctx.send(f"Sorry, You cannot {ctx.command.name} someone who has the same role as you...")
        if ctx.author.top_role < member.top_role:
            await ctx.send(f"Sorry, but you can't {ctx.command.name} someone with a higher role than you...")
    except Exception:
        pass


def can_handle(ctx, permission: str):
    return isinstance(ctx.channel, discord.DMChannel) or getattr(ctx.channel.permissions_for(ctx.guild.me), permission)
