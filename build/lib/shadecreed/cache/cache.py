import os,sys,json
from shadecreed.ux.anime import wr,wrdel,wrcold
from shadecreed.ux.process import processContent
from shadecreed.core.utils.base import base_dir,cache_dir,onload_file
from shadeDB.core import shadeDB
from shadecreed.core.utils.base import cacheStorage

class cache:
  def __init__(self,session_target,data,response):
    self.session_target = session_target
    self.data = dict(data)
    self.response = response
    self.store()
    
  def store(self):
    init = {'target': self.session_target,'content-size':len(self.response.content),'elapsed-time':f'{self.response.elapsed}'}
    for k, v in self.data.items():
      init.update({k : v})
    if init:
      cacheStorage.import_dict(init)
      #wrdel('[+] Server headers received', '[+] Data stored as cache 📜')
      processContent(self.response,f'{cache_dir}/page.html')
        
  def active(self):
    res = cacheStorage.export_dict()
    if res['target'] == self.session_target:
      return True
    else:
      return None
  
  def read(self):
    if self.active():
      return cacheStorage.export_dict()
      
  def clear(self):
    del_each = [f'{cache_dir}/cache.scdb',f'{cache_dir}/page.html',f'{base_dir}/core/utils/*.scdb']
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