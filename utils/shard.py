import discord

from utils import checks
from discord.ext.commands import AutoShardedBot


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not checks.can_handle(msg, "send_messages"):
            return

        await self.process_commands(msg)


