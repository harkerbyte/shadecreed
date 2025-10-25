import sys
from shadecreed.core.utils.base import home,stream,write_statistics,cache_dir,required_modules
from shadecreed.ux.anime import wr

home.mkdir(parents=True,exist_ok=True)
stream.mkdir(parents=True,exist_ok=True)

write_statistics()
"""
def check():
  for each in required_modules:
    try:
      import each
    except Exception as error:
      wr(f'Missing... ` pip {each} ` to install')
      print(error)
      if each == required_modules[-1]:
        sys.exit()
      continue
check()
"""
