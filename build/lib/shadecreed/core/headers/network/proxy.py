import httpx,random,os,json
from shadecreed.ux.anime import wr
from shadecreed.core.utils.base import base_dir,cache_dir

def proxUse():
  if os.path.exists(f'{base_dir}/proxy.txt'):
    with open(f'{base_dir}/proxy.txt', 'r') as format_:
      line = [line.strip() for line in format_.readlines() if line]
      return line
  else:
    return None        
    
def proxyParse(use):
  if use is not None:
    return {'http://' : f'http://{use}','https://' : f'https://{use}'}
  else:
    return None


def readCache(content=False):
  if content == False:
    with open(f'{cache_dir}/cache.json','r') as file:
      cache = json.load(file)
      return cache
  else:
    if os.path.exists(f'{cache_dir}/page.html'):
      with open(f'{cache_dir}/page.html') as content:
        return content.read()
    else:
      return None
    
def proxyTest():
  proxyused,instance,config = proxyParse(),readCache(),map()
  for _ in range(5):
    try:
      test = httpx.request(config.get('method', 'GET').upper(), instance['target'], proxy=proxyused, timeout=5,follow_redirects=True)
      if proxyused and test.status_code == 200:
        wr('\033[1;32m[+] Connection Secured ✅ \033[1;0m]')
        return proxyused
    except Exception:
      continue
  
  return None