import dbl
import discord
from discord.ext import commands, tasks
from os import environ as env
from dotenv import load_dotenv
import asyncio
import logging


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = env.get("DBLToken") 
        self.dblpy = dbl.DBLClient(self.bot, self.token)

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

        await asyncio.sleep(1800)

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(TopGG(bot))
