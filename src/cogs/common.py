from speedtest import Speedtest
from pathlib import Path
from discord.ext import commands
import discord, os, json, yaml, time, colors

from src.utils import _print, DEBUG

class Common(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        try:
            with open(Path(os.path.dirname(__file__)).joinpath('onStart.json'), 'r', encoding='utf-8') as f:
                self.onStart = json.loads(f.read())
        except Exception as e:
            print(e)
            self.newJson(False, 1)
        
        with open(Path(os.path.dirname(__name__)).joinpath('config.yaml'), 'r') as f:
            config = yaml.safe_load(f)
        DEBUG: bool = config['debug']
    
    def newJson(self, reboot, id):
        self.onStart = {
            'reboot':reboot,
            'id':id
        }
        with open(Path(os.path.dirname(__file__)).joinpath('onStart.json'), 'w', encoding='utf-8') as f:
            json.dump(self.onStart, f)
    
    @commands.Cog.listener()    
    async def on_ready(self):
        _print('Logged in as', self.bot.user.name)
        _print('Bot id', str(self.bot.user.id))
        _print('API version', discord.__version__)
        await self.bot.change_presence(status=discord.Status.idle)
        synced = await self.bot.tree.sync()
        _print('Commands synced', str(len(synced)))
        ac = discord.Game(name='/help')
        await self.bot.change_presence(status=discord.Status.online, activity=ac)
        if self.onStart['reboot']:
            await self.bot.get_channel(self.onStart['id']).send('Sucesfully rebooted')
        self.newJson(False, 1)
        _print('Bot is online' ,'^.^')

    @discord.app_commands.command(name='ping', description='Show bot latency and server\'s internet speed')
    async def ping(self, inter: discord.Interaction):
        _print('Command triggred: ', 'ping')
        sp = Speedtest()
        em = discord.Embed()
        em.title = 'Internet speed'
        em.color = 0x1a1a41
        em.add_field(name='Latency', 
                    value=f'{round(self.bot.latency*1000)} ms')
        em.add_field(name='Download', 
                    value='--- Mb/s')
        em.add_field(name='Upload',
                    value='--- Mb/s')
        await inter.response.send_message(embed=em)
        async with inter.channel.typing():
            em.set_field_at(1, name='Download', 
                            value=f'{round(sp.download()/1000/1000, 2)} Mb/s')
            await inter.edit_original_response(embed=em)
        async with inter.channel.typing():
                em.set_field_at(2, name='Upload', 
                            value=f'{round(sp.upload()/1000/1000, 2)} Mb/s')
                await inter.edit_original_response(embed=em)
        if DEBUG:
            exit()
        
    @discord.app_commands.command(name='reboot', description='Reboot server')
    async def reboot(self, inter: discord.Interaction):
        _print('Command triggred: ', 'reboot')
        await inter.response.send_message('Rebooting...')
        self.newJson(True, int(inter.channel_id))
        if DEBUG:
            exit()
        else:
            os.system('sudo reboot')
            _print('rebooting')
    
    @discord.app_commands.command(name='help', description='Show all commands available')
    @discord.app_commands.describe(command='Commands to choose from')
    @discord.app_commands.choices(command=[
        discord.app_commands.Choice(name='help', value='help'),
        discord.app_commands.Choice(name='ping', value='ping'),
        discord.app_commands.Choice(name='reboot', value='reboot'),
        discord.app_commands.Choice(name='download', value='download')
    ])
    async def help(self, inter: discord.Interaction, command:discord.app_commands.Choice[str]=None):
        _print('Command triggred: ', 'help')
        em = discord.Embed()
        em.color = 0xffee00
        if not command:   
            em.title = f'Commands for {self.bot.user.name}\n'
            em.description = f'''
            Use prefix `/`
            For advanced description type `/help <command>` (`/help ping`)
            '''
            for commands in self.bot.tree.get_commands():
                em.add_field(name=commands.name, value=commands.description, inline=False)
            await inter.response.send_message(embed=em)
        else:
            for commands in self.bot.tree.get_commands():
                if commands.name.lower() == str(command.name).lower():
                    em.title = f'{commands.name}'
                    em.description = f'{commands.description}'
                    await inter.response.send_message(embed=em)
                    break
            else:
                em.title = 'Error 404'
                em.description = f'Command `/help {command.name}` not found!\nTry `/help`'
                em.color = 0xff0000
                await inter.response.send_message(embed=em)

        if DEBUG:
            exit()

async def setup(bot: commands.Bot):
    await bot.add_cog(Common(bot))