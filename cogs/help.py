import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
      embed = discord.Embed(
        description="Type `;;help <section>` for more infromation on that topic.",
        color=discord.Colour.blurple()
      )
      embed.set_thumbnail(url=self.bot.user.avatar_url)
      embed.add_field(name="Sections", value="**`Moderation`**\n**`Setup`**\n**`Utility`**", inline=True)
      embed.set_author(name="Help Menu", icon_url=ctx.guild.icon_url)
      embed.set_footer(text=f"Command Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.reply(embed=embed)

    @help.command(name="moderation", aliases=["Mod", "Moderation", "mod"])
    async def mod_(ctx):
      await ctx.send("__**Moderation Commands**__\n\n`kick`\n`ban`") 
    
    @help.command(name="setup",aliases=["Setup"])
    async def setup_(self, ctx):
      await ctx.send("__**Setup Commands**__\n\n`setup`\n")
    
    @help.command(name="Utility",aliases=["utils", "Utils", "utility"])
    async def mod_(self, ctx):
      await ctx.send("__**Utility Commands**__\n\n`ping`\n")


def setup(bot):
  bot.add_cog(Help(bot))