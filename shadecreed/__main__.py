import os,httpx,sys,threading,time,argparse,subprocess
from bs4 import BeautifulSoup as bs
from shadecreed.cache.cache import cache
from shadecreed.ux.anime import wr,wrdel,wrdic,wrcold
from shadecreed.ux.ascii import banner,menu
from shadecreed.core.headers.argue import headerEditor
from shadecreed.core.utils.assemble import startAssembling
from shadecreed.core.middleware.drive import drive
from shadecreed.core.utils.build import buildXss
from shadecreed.core.utils.base import base_dir,cache_dir
gr = '\033[1;32m'
pl = '\033[1;0m'
ye = '\033[1;33m'
sp = """
 _, __, _,  _ _, _ ___ __, __,
(_  |_) |   | |\\ |  |  |_  |_)
, ) |   | , | | \\|  |  |   | \\
 ~  ~   ~~~ ~ ~  ~  ~  ~~~ ~ ~
"""

class main:
  def __init__(self,target):
    self.target = target
    self.sl(banner())
    self.sl(menu(self.target))
    self.cont()
   
  def sl(self,te,ti=0.0003):
    for ie in te:
      sys.stdout.write(ie)
      sys.stdout.flush()
      time.sleep(ti)
    sys.stdout.write(pl+'\n')
  
  def sldel(self,te,re,ti=0.005):
    for ie in te:
      sys.stdout.write(ie)
      sys.stdout.flush()
      time.sleep(ti)
      
    sys.stdout.write(f'\r')
    for i in range(len(re)):
      sys.stdout.write(f'\r{re[:i+1]}' + ' ' * (len(te)-i-1))
      sys.stdout.flush()
      time.sleep(ti)
    sys.stdout.write('\n')
  
  def fiforms(self,res,read='[+] Scanning for forms'):
    global ac_forms
    for parser in ['html.parser','html5lib']:
      inspect = bs(res.text, parser)
      ac_forms =  inspect.find_all('form')
      if ac_forms:
        break
    if ac_forms:
      self.sldel(read,'[+] Forms were found ✅')
    else:
      self.sldel(read, '[-] No forms were found ❌')
    
  def cont(self):
    try:
      self.sl('[+] Attempting to establish an initial connection',ti=0.005)
      re = httpx.request('GET',self.target,follow_redirects=True)
      if re.status_code == 200:
        self.sl('[+] Connection established ✅')
      self.fiforms(re)
      global cache
      cache = cache(self.target,re.headers,re)
    except Exception as er:
      print(er)
      sys.exit()

def start():
  parse = argparse.ArgumentParser(description="A cli web application pentesting toolkit. Seem you intend to start the whole framework, that\'s great 🗿")
  parse.add_argument('-u','--url',help="<target_url>",required=True)
  parse.add_argument('-v','--version',action="version",version="shadecreed - 0.13.7",help="Display framework version")
  args = parse.parse_args()
  
  if args.url:
    if args.url.startswith('http'):
      main(args.url)
    else:
      wr(f'{args.url} is an invalid http address')
      sys.exit()
  
    sys.stdout.write('\n')
    while True:
      opt = input('>>> ').strip()
      if opt.lower() == 'h':
        if cache.active():
          headerEditor()
      elif opt.lower() == 'b':
        if ac_forms:
          document = open(f'{cache_dir}/page.html','r')
          startAssembling(document)
        else:
          wrcold('No forms was detected on the page',co='\x1b[1;31m',timeout=1.5)
      elif opt.lower() == 'x':
        buildXss()
      elif opt.lower() == 'j':
        subprocess.run(['xdg-open', 'https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S'])
      elif opt.lower() == 'q':
        cache.clear()
      elif opt != '':
        wrcold(f'{opt} is an unknown command',co='\x1b[1;31m',reverse=True)      
if __name__ == "__main__":
  pass
      
  