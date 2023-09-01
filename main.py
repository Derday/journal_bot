from discord.ext import commands
from pathlib import Path
import discord, os, asyncio

from src.utils import _print, TOKEN, PRFX

class Main:
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(intents=intents, command_prefix=PRFX, help_command=None)
        asyncio.run(self.main())

    async def load(self):
        for filename in os.listdir(Path(os.path.dirname(__file__)).joinpath('src').joinpath('cogs')): # for multiplatform compatibility
            if filename.endswith('.py'):
                _print('Loading cog', filename)
                await self.bot.load_extension(f'src.cogs.{filename[:-3]}')

    async def main(self):
        await self.load()
        _print('Running', __name__)
        await self.bot.start(TOKEN)

if __name__ == '__main__':
    Main()