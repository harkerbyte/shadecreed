import os,sys,json
from shadecreed.ux.anime import wr,wrdel,wrcold
from shadecreed.ux.process import processContent
from shadecreed.core.utils.base import base_dir,cache_dir

class cache:
  def __init__(self,session_target,data,response):
    self.session_target = session_target
    self.data = dict(data)
    self.response = response
    self.store()
   
  def write(self):
    if not os.path.exists(f'{cache_dir}/cache.json'):
      with open(f'{cache_dir}/cache.json','w') as in_:
        in_.write('{}')
        in_.close()
      return True
    return ['q']
    
  def store(self):
    init = {'target': self.session_target,'content-size':len(self.response.content),'elapsed-time':f'{self.response.elapsed}'}
    for k, v in self.data.items():
      init.update({k : v})
    if self.write():
      with open(f'{cache_dir}/cache.json', 'w') as st:
        json.dump(init, st, indent=2)
      
      wrdel('[+] Server headers received', '[+] Data stored as cache 📜')
      processContent(self.response,f'{cache_dir}/page.html')
        
  def active(self):
    with open(f'{cache_dir}/cache.json', 'r') as re:
      res = json.load(re)
      try:
        if res['target'] == self.session_target:
          return True
      except KeyError:
        return None
  
  def read(self):
    if self.rmdr():
      with open(f'{cache_dir}/cache.json', 'r') as re:
        res = json.load(re)
        return res
      
      
  def clear(self):
    del_each = [f'{cache_dir}/cache.json',f'{cache_dir}/page.html',f'{base_dir}/core/utils/*.json']
    for each in del_each:
      try:
        os.path.remove(each)
        del_each.remove(each)
      except Exception:
        continue
    if not del_each:
      wrcold('Cache cleared',co='\x1b[1;31m',timeout=2)
    sys.exit()
 
      
if __name__ == '__main__':
  cache()