from pathlib import Path
import colors, time, os, yaml

def _print(msg: str, value: str = None):
    if not msg.endswith(' '):
        msg+=' '
    if value:
        print(colors.green(time.strftime('[%H:%M:%S]', time.localtime())) + colors.white(msg) + colors.yellow(value))
    else:
        print(colors.green(time.strftime('[%H:%M:%S]', time.localtime())) + colors.white(msg))

with open(Path(os.path.dirname(__name__)).joinpath('config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
DEBUG: bool = config['debug']
TOKEN: str  = config['token']
PRFX:  str  = config['prfx']