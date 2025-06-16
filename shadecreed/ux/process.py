import re,os,json,threading,datetime
from bs4 import BeautifulSoup as bs
from shadecreed.ux.anime import wr,wrdic,wrcom
from shadecreed.core.headers.network.proxy import readCache
from shadecreed.core.utils.base import base_dir,cache_dir,stream_dir,onload_file

key_headers = ['Location', 'Set-Cookie', 'Content-Security-Policy', 'Access-Control-Allow-Origin']

def skim(target):
  if target.startswith('http'):
    try:
      host, end = target.split('.',1)
      proto, dns = host.split('//',1)
      return dns
    except Exception:
      return None
      
def processResponse(response):
  cache = readCache()
  custom_headers = onload_file(f'{base_dir}/core/headers/map.json')
  available = dict()
  if response.status_code:
    available['[+] Status code'] = response.status_code
  if response.encoding:
    available['[+] Encoding'] = response.encoding
  if response.elapsed:
    available['[+] Elapsed time'] = response.elapsed  
  if response.url:
    available['[+] Final url'] = response.url
  if response.history:
    available['[+] Status history'] = [x.status_code for x in response.history]
  if response.cookies:
    available['[+] Cookies'] = response.cookies
  if response.content:
    available['[+] Content (byte)'] = len(response.content)
    #if len(response.content) < int(cache['content-size']):
     # wr('[+] Noticeable change in content size ✅')
      #ask = input('[+] Would you like to observe this `Yes/No`: ')
     # if ask.lower() == 'yes':
     #   content = readCache(content=True)
      #  wr(response.text[:300],ti=0.0005)
    #  else:
       # pass
  try:
    if custom_headers['host'] in response.text:
      wr(f'{cache['host']} spotted in page body')
  except Exception:
    pass
  
  for key in response.headers:
    if key in key_headers:
      available[key] = value
      
  wrdic(available)
  
def processContent(response,saveTo):
  use_cache = readCache()
  if 'html' in use_cache['content-type']:
    html = bs(response.text, 'html.parser')
    wr(f'[+] Page content type : {use_cache['content-type']} 📜')
    if saveTo:
      with open(saveTo,'w') as save:
        save.write(html.prettify())
        save.close()
      
  else:
    wr(f'[+] Page content type : {use_cache['content-type']} 📜')
  wr(f'[+] Page elapsed time : {use_cache['elapsed-time']}')
  wr(f'[+] Page content size (byte) : {len(response.content)} 📜')
  
class streamData:
  def __init__(self,data,streamed=None):
    self.data = data if isinstance(data, dict) else dict(data)
    self.streamed = streamed if streamed != None else dict()
    self.keep_alive = None
    self.process()
    
  def writejson(self):
    with open(f'{stream_dir}/streamed.json', 'w') as write:
      json.dump(f'{{}}', write)
      
  def process(self):
    if os.path.exists(f'{base_dir}/core/middleware/process.json'):
      status = onload_file(f'{base_dir}/core/middleware/process.json')
      self.keep_alive = status['keep-alive']
    else:
       self.keep_alive = False
      
  def streaming(self):
    if isinstance(self.data, dict):
      for key, value in self.data.items():
        if self.keep_alive:
          wr('%s : %s'%(key, value))
      
  def conclude(self):
    while True:
      if os.path.exists(f'{stream_dir}/streamed.json'):
        try:
          existing_data = onload_file(f'{stream_dir}/streamed.json')
          with open(f'{stream_dir}/streamed.json', 'w') as rewrite:
            existing_data.update(self.streamed)
            json.dump(existing_data, rewrite, indent=2)
            break
        except Exception as error:
          print(error)
          self.writejson()
      else:
        self.writejson()
        
    