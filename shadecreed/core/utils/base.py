import os,sys,json,argparse
from pathlib import Path
from shadecreed.ux.anime import wr,wrdic

#Fixed dirs
navigate = Path.home()
home_dir = navigate / ".shadecreed" / "logs"
stream_dir = home_dir / "stream"

#Temp dirs
base_dir = Path(__file__).resolve().parents[2]
cache_dir = base_dir / 'cache'
password_dir = base_dir / 'path'


def onload_file(onload):
  if os.path.isfile(onload):
    if '/' in onload:
      target = onload.split('/')[-1:]
      file = target[0]
    name, ext = os.path.splitext(file)
    if ext == '.json':
      with open(onload, 'r') as loaded:
        try:
          return json.load(loaded)
        except JSONDecodeError:
          return '{}'
    else:
      wr(f'{file.split('/')[-1:]} carries an invalid extension for a json document')
      sys.exit()
  else:
    raise FileNotFoundError(f'{onload} was not found')

"""    
def readXssLog():
  parse = argparse.ArgumentParser(description="Read xss captured datas")
  parse.add_argument('-r','--read',help="Provide the number of recent datas to display - LIFO")
  args = parse.parse_args()
  
  if os.path.exists(stream_dir / 'streamed.json'):
    retrieved = onload_file(stream_dir / 'streamed.json')
    if args.read and args.read >= 1:
      Lifo = retrieved.items()[-args.read:]
    else:
      Lifo = retrieved.items()[-5:]
      
    wrdic(Lifo)
  else:
    wr(f'There are no existing log')
"""